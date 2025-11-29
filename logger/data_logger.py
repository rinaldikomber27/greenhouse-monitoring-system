"""
Data Logger Service - Distributed System Component
===================================================
This service operates as an independent distributed process that:
1. Subscribes to all MQTT topics (message passing)
2. Persists sensor data to MongoDB
3. Runs independently without shared memory
4. Demonstrates loose coupling in distributed architecture
"""

import paho.mqtt.client as mqtt
import json
import os
import time
from pymongo import MongoClient
from datetime import datetime


class DataLogger:
    """
    Autonomous Data Logger - Distributed Service
    Subscribes to MQTT and persists data
    """
    
    def __init__(self, mqtt_broker, mqtt_port, mongo_host, mongo_port):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        
        self.mqtt_client = None
        self.mongo_client = None
        self.db = None
        
        print("[DATA-LOGGER] Initializing distributed data logger service...")
    
    def connect_mongodb(self):
        """Connect to MongoDB"""
        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.mongo_client = MongoClient(
                    f'mongodb://{self.mongo_host}:{self.mongo_port}/',
                    serverSelectionTimeoutMS=3000
                )
                # Test connection
                self.mongo_client.server_info()
                self.db = self.mongo_client['sensor_data']
                print(f"[DATA-LOGGER] ✅ Connected to MongoDB at {self.mongo_host}:{self.mongo_port}")
                return True
            except Exception as e:
                retry_count += 1
                print(f"[DATA-LOGGER] MongoDB connection attempt {retry_count}/{max_retries} failed: {e}")
                time.sleep(3)
        
        return False
    
    def connect_mqtt(self):
        """Connect to MQTT Broker"""
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("[DATA-LOGGER] ✅ Connected to MQTT Broker")
                
                # Subscribe to all topics
                client.subscribe('env/#')
                print("[DATA-LOGGER] 📡 Subscribed to: env/#")
            else:
                print(f"[DATA-LOGGER] Failed to connect, return code {rc}")
        
        def on_message(client, userdata, msg):
            try:
                data = json.loads(msg.payload.decode())
                self.save_data(msg.topic, data)
            except Exception as e:
                print(f"[DATA-LOGGER] Error processing message: {e}")
        
        self.mqtt_client = mqtt.Client(client_id='data-logger-service')
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message
        
        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, keepalive=60)
                self.mqtt_client.loop_start()
                print("[DATA-LOGGER] MQTT connection established")
                return True
            except Exception as e:
                retry_count += 1
                print(f"[DATA-LOGGER] MQTT connection attempt {retry_count}/{max_retries} failed: {e}")
                time.sleep(3)
        
        return False
    
    def save_data(self, topic, data):
        """Save data to MongoDB"""
        try:
            # Add metadata
            data['topic'] = topic
            data['logged_at'] = datetime.now()
            
            # Determine collection based on topic
            if '/event/' in topic:
                collection = self.db['events']
            else:
                collection = self.db['sensor_readings']
            
            # Insert document
            result = collection.insert_one(data)
            print(f"[DATA-LOGGER] 💾 Saved: {topic} | {data.get('sensor')} = {data.get('value')} | Node: {data.get('node')}")
            
        except Exception as e:
            print(f"[DATA-LOGGER] Error saving data: {e}")
    
    def start(self):
        """Start the data logger service"""
        # Connect to MongoDB
        if not self.connect_mongodb():
            print("[DATA-LOGGER] Failed to connect to MongoDB. Exiting.")
            return
        
        # Connect to MQTT
        if not self.connect_mqtt():
            print("[DATA-LOGGER] Failed to connect to MQTT broker. Exiting.")
            return
        
        print("[DATA-LOGGER] ✅ Data logger service fully operational")
        print("[DATA-LOGGER] Listening for distributed sensor data...")
        
        # Keep service alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[DATA-LOGGER] Shutting down gracefully...")
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self.mongo_client.close()


if __name__ == "__main__":
    # Get configuration from environment
    mqtt_broker = os.getenv('MQTT_BROKER', 'mqtt-broker')
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    mongo_host = os.getenv('MONGO_HOST', 'db-logger')
    mongo_port = int(os.getenv('MONGO_PORT', 27017))
    
    print("=" * 70)
    print("DISTRIBUTED DATA LOGGER SERVICE")
    print("=" * 70)
    print(f"MQTT Broker: {mqtt_broker}:{mqtt_port}")
    print(f"MongoDB: {mongo_host}:{mongo_port}")
    print("Architecture: Message Passing + Persistence Layer")
    print("=" * 70)
    
    # Create and start logger
    logger = DataLogger(mqtt_broker, mqtt_port, mongo_host, mongo_port)
    logger.start()
