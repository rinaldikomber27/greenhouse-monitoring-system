"""
Edge Computing Node - Distributed Sensor Monitoring System
============================================================
This module implements an autonomous edge computing node that:
1. Runs concurrent threads for multiple sensors (distributed computing)
2. Performs local computation and constraint checking (edge computing)
3. Communicates via MQTT message passing (no shared memory)
4. Implements event-driven architecture for alerts
5. Operates independently as a distributed process

Architecture:
- Each sensor runs in its own thread (concurrency)
- No shared memory between containers
- All communication via MQTT publish-subscribe
- Event-driven trigger when constraints violated
"""

import paho.mqtt.client as mqtt
import json
import random
import time
import threading
import os
from datetime import datetime


class EdgeSensorNode:
    """
    Autonomous Edge Computing Node
    Implements distributed system principles:
    - Message passing via MQTT (no shared memory)
    - Concurrent processing (multi-threading)
    - Event-driven architecture
    - Loose coupling with other services
    """
    
    def __init__(self, node_id, mqtt_broker, mqtt_port=1883):
        self.node_id = node_id
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.client = None
        
        # Sensor constraints (Edge Computing Logic)
        self.constraints = {
            'temperature': {'min': 15, 'max': 30},
            'humidity': {'min': 40, 'max': 80},
            'light': {'min': 100},
            'airquality': {'max': 1000}
        }
        
        # Sensor intervals (seconds) - Updated for better visibility
        self.intervals = {
            'temperature': 20,   # 20 seconds = 3 data points per minute
            'humidity': 20,      # 20 seconds = 3 data points per minute
            'light': 20,         # 20 seconds = 3 data points per minute
            'airquality': 20     # 20 seconds = 3 data points per minute
        }
        
        # Simulation mode flags
        self.simulation_mode = None
        
        print(f"[{self.node_id}] Edge Computing Node Initializing...")
        
    def connect_mqtt(self):
        """Establish MQTT connection for message passing"""
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"[{self.node_id}] Connected to MQTT Broker (Message Passing Hub)")
                # Subscribe to control topic for simulation commands
                client.subscribe("greenhouse/control/simulate")
                print(f"[{self.node_id}] Subscribed to control topic")
            else:
                print(f"[{self.node_id}] Failed to connect, return code {rc}")
        
        def on_message(client, userdata, msg):
            """Handle incoming control messages"""
            try:
                data = json.loads(msg.payload.decode())
                sim_type = data.get('type')
                print(f"[{self.node_id}] Received simulation command: {sim_type}")
                self.simulation_mode = sim_type
            except Exception as e:
                print(f"[{self.node_id}] Error processing control message: {e}")
        
        self.client = mqtt.Client(client_id=f"{self.node_id}")
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        
        # Connect with retry logic
        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.client.connect(self.mqtt_broker, self.mqtt_port, keepalive=60)
                self.client.loop_start()
                print(f"[{self.node_id}] MQTT connection established")
                return True
            except Exception as e:
                retry_count += 1
                print(f"[{self.node_id}] Connection attempt {retry_count}/{max_retries} failed: {e}")
                time.sleep(3)
        
        return False
    
    def simulate_sensor_reading(self, sensor_type):
        """Simulate sensor reading (in real system, this would read actual sensors)"""
        # Check if simulation mode is active
        if self.simulation_mode == 'overheat':
            if sensor_type == 'temperature':
                return round(random.uniform(32, 36), 2)  # Force high temperature
        elif self.simulation_mode == 'lowlight':
            if sensor_type == 'light':
                return round(random.uniform(30, 80), 2)  # Force low light
        elif self.simulation_mode == 'poorair':
            if sensor_type == 'airquality':
                return round(random.uniform(1100, 1400), 2)  # Force poor air quality
        elif self.simulation_mode == 'reset':
            # Normal readings for reset
            pass
        
        # Normal readings
        readings = {
            'temperature': random.uniform(10, 35),  # °C
            'humidity': random.uniform(30, 90),     # %
            'light': random.uniform(50, 500),       # lumens
            'airquality': random.uniform(500, 1500) # ppm
        }
        return round(readings[sensor_type], 2)
    
    def check_constraint(self, sensor_type, value):
        """
        Edge Computing: Local constraint checking
        Returns (is_event, event_type)
        """
        constraint = self.constraints[sensor_type]
        
        if sensor_type == 'temperature':
            if value > constraint['max']:
                return True, 'temperature_alert_high'
            elif value < constraint['min']:
                return True, 'temperature_alert_low'
        
        elif sensor_type == 'humidity':
            if value > constraint['max']:
                return True, 'humidity_alert_high'
            elif value < constraint['min']:
                return True, 'humidity_alert_low'
        
        elif sensor_type == 'light':
            if value < constraint['min']:
                return True, 'light_low'
        
        elif sensor_type == 'airquality':
            if value > constraint['max']:
                return True, 'airquality_warning'
        
        return False, None
    
    def publish_data(self, sensor_type, value, is_event, event_type):
        """
        Publish data via MQTT (Message Passing)
        - Normal data → raw channel
        - Event data → event channel (Event-Driven Architecture)
        """
        timestamp = datetime.now().isoformat()
        
        # Prepare payload
        payload = {
            'sensor': sensor_type,
            'value': value,
            'timestamp': timestamp,
            'node': self.node_id,
            'event': is_event,
            'event_type': event_type if is_event else None
        }
        
        # Publish to raw channel (always)
        raw_topic = f"env/{sensor_type}/raw"
        self.client.publish(raw_topic, json.dumps(payload))
        
        # Publish to event channel (if constraint violated)
        if is_event:
            event_topic = f"env/event/{event_type}"
            self.client.publish(event_topic, json.dumps(payload))
            print(f"[{self.node_id}] 🚨 EVENT TRIGGERED: {event_type} | Value: {value}")
        else:
            print(f"[{self.node_id}] 📊 Normal reading: {sensor_type}={value}")
    
    def sensor_thread(self, sensor_type):
        """
        Concurrent sensor thread (Distributed Computing)
        Each sensor operates independently in its own thread
        """
        print(f"[{self.node_id}] Thread started for {sensor_type} sensor (interval: {self.intervals[sensor_type]}s)")
        
        while True:
            try:
                # Edge Computing: Read and process sensor data locally
                value = self.simulate_sensor_reading(sensor_type)
                
                # Edge Computing: Local constraint checking
                is_event, event_type = self.check_constraint(sensor_type, value)
                
                # Message Passing: Publish via MQTT
                self.publish_data(sensor_type, value, is_event, event_type)
                
                # Sleep according to sensor interval
                time.sleep(self.intervals[sensor_type])
                
            except Exception as e:
                print(f"[{self.node_id}] Error in {sensor_type} thread: {e}")
                time.sleep(5)
    
    def start(self):
        """
        Start the edge computing node with concurrent threads
        """
        # Connect to MQTT broker (message passing hub)
        if not self.connect_mqtt():
            print(f"[{self.node_id}] Failed to connect to MQTT broker. Exiting.")
            return
        
        print(f"[{self.node_id}] Starting concurrent sensor threads...")
        
        # Create and start independent threads for each sensor
        sensors = ['temperature', 'humidity', 'light', 'airquality']
        threads = []
        
        for sensor in sensors:
            thread = threading.Thread(
                target=self.sensor_thread,
                args=(sensor,),
                daemon=True,
                name=f"{self.node_id}-{sensor}"
            )
            thread.start()
            threads.append(thread)
        
        print(f"[{self.node_id}] ✅ Edge Computing Node fully operational")
        print(f"[{self.node_id}] All {len(threads)} sensor threads running concurrently")
        print(f"[{self.node_id}] Message passing via MQTT on broker: {self.mqtt_broker}")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n[{self.node_id}] Shutting down gracefully...")
            self.client.loop_stop()
            self.client.disconnect()


if __name__ == "__main__":
    # Get configuration from environment (container environment)
    node_id = os.getenv('NODE_ID', 'edge-1')
    mqtt_broker = os.getenv('MQTT_BROKER', 'mqtt-broker')
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    
    print("=" * 70)
    print("DISTRIBUTED EDGE COMPUTING NODE")
    print("=" * 70)
    print(f"Node ID: {node_id}")
    print(f"MQTT Broker: {mqtt_broker}:{mqtt_port}")
    print(f"Architecture: Event-Driven + Message Passing")
    print("=" * 70)
    
    # Create and start edge node
    edge_node = EdgeSensorNode(node_id, mqtt_broker, mqtt_port)
    edge_node.start()
