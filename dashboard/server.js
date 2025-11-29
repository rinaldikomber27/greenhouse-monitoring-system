/**
 * Monitoring Dashboard Server - Distributed System
 * =================================================
 * Real-time monitoring dashboard that:
 * 1. Subscribes to MQTT topics (message passing)
 * 2. No direct connection to edge nodes (distributed principle)
 * 3. Broadcasts data to web clients via WebSocket
 * 4. Displays real-time graphs and event alerts
 */

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const mqtt = require('mqtt');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Serve static files
app.use(express.static('public'));

// MQTT Configuration (from container environment)
const MQTT_BROKER = process.env.MQTT_BROKER || 'mqtt-broker';
const MQTT_PORT = process.env.MQTT_PORT || 1883;
const mqttUrl = `mqtt://${MQTT_BROKER}:${MQTT_PORT}`;

console.log('='.repeat(70));
console.log('DISTRIBUTED MONITORING DASHBOARD');
console.log('='.repeat(70));
console.log(`Connecting to MQTT Broker: ${mqttUrl}`);
console.log('Architecture: Message Passing via MQTT (no shared memory)');
console.log('='.repeat(70));

// Connect to MQTT Broker (Message Passing Hub)
const mqttClient = mqtt.connect(mqttUrl, {
    clientId: 'dashboard-subscriber-' + Math.random().toString(16).substr(2, 8),
    reconnectPeriod: 3000
});

mqttClient.on('connect', () => {
    console.log('✅ Connected to MQTT Broker');
    console.log('📡 Subscribing to sensor topics...');
    
    // Subscribe to all raw data channels
    mqttClient.subscribe('env/+/raw', (err) => {
        if (!err) {
            console.log('✅ Subscribed to: env/+/raw');
        }
    });
    
    // Subscribe to all event channels
    mqttClient.subscribe('env/event/#', (err) => {
        if (!err) {
            console.log('✅ Subscribed to: env/event/#');
        }
    });
    
    console.log('🚀 Dashboard is now receiving distributed sensor data');
});

mqttClient.on('error', (error) => {
    console.error('❌ MQTT Error:', error);
});

// Handle incoming MQTT messages (Message Passing)
mqttClient.on('message', (topic, message) => {
    try {
        const data = JSON.parse(message.toString());
        
        // Broadcast to all connected web clients via WebSocket
        if (topic.includes('/raw')) {
            io.emit('sensor_data', data);
        } else if (topic.includes('/event/')) {
            io.emit('sensor_event', data);
            console.log(`🚨 Event received: ${data.event_type} from ${data.node}`);
        }
    } catch (error) {
        console.error('Error parsing MQTT message:', error);
    }
});

// WebSocket connection handling
io.on('connection', (socket) => {
    console.log('👤 Client connected to dashboard');
    
    // Handle simulation commands from dashboard
    socket.on('simulation', (data) => {
        console.log(`🎮 Simulation command received: ${data.type}`);
        
        // Publish simulation command to MQTT for edge nodes
        const command = {
            type: data.type,
            timestamp: new Date().toISOString()
        };
        
        mqttClient.publish('greenhouse/control/simulate', JSON.stringify(command));
        console.log(`📤 Simulation command sent to edge nodes via MQTT`);
    });
    
    socket.on('disconnect', () => {
        console.log('👤 Client disconnected');
    });
});

// Main dashboard route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
const PORT = 3000;
server.listen(PORT, '0.0.0.0', () => {
    console.log(`🌐 Dashboard server running on http://0.0.0.0:${PORT}`);
    console.log(`📊 Open in browser: http://localhost:${PORT}`);
});
