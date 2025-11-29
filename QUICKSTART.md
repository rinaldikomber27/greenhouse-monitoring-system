# Quick Start Guide - Greenhouse Environmental Monitoring System

## 🚀 Quick Start (5 Minutes)

### 1. Start the System
```bash
cd mqtt-env-monitoring
./start.sh
```

OR manually:
```bash
docker-compose up --build -d
```

### 2. Open Dashboard
Open browser: **http://localhost:3000**

You should see:
- 4 real-time **historical graphs** with time-series visualization (temperature, humidity, light, air quality)
- **Time range selector** (5 min / 15 min / 1 hour views)
- **Smart Control Panel** with recommended actions for each sensor type
- **Simulation buttons** to trigger test scenarios
- **Real-time event alert panel** with detailed recommendations
- **10 Recent Updates** panel showing latest sensor data and events
- Status bar with live metrics

### 3. Watch the Magic ✨

The system will automatically:
- ✅ Start 2 greenhouse zones (edge-1, edge-2)
- ✅ Begin sensor readings every 5-10 seconds
- ✅ Display data in real-time **historical time-series graphs**
- ✅ Trigger alerts when constraints violated
- ✅ Show **recommended automation actions** for each alert
- ✅ Support **interactive simulation controls**
- ✅ Save all data to MongoDB

### 4. Try Interactive Features 🎮

**Time Range Selection:**
- Click "5 Minutes", "15 Minutes", or "1 Hour" to change graph view
- All 4 graphs update automatically with historical data

**Simulation Controls:**
- Click "🔥 Simulate Overheat" to force temperature alerts
- Click "🌙 Simulate Low Light" to trigger light warnings
- Click "💨 Simulate Poor Air Quality" to test air quality alerts
- Click "🔄 Reset to Normal" to return to standard operation

**Smart Automation:**
- View recommended actions for each sensor type
- See real-time control suggestions when alerts trigger

---

## 📊 What You'll See

### Normal Operation
```
[edge-1] 📊 Normal reading: temperature=25.3
[edge-1] 📊 Normal reading: humidity=55.8
[edge-1] 📊 Normal reading: light=250.5
[edge-1] 📊 Normal reading: airquality=750.2
```

### Event Triggered (Alert)
```
[edge-1] 🚨 EVENT TRIGGERED: temperature_alert_high | Value: 32.5
[edge-2] 🚨 EVENT TRIGGERED: airquality_warning | Value: 1150.3
```

Dashboard will show:
- 🔴 Red alert panel with event details
- 📈 Spike in the graph
- ⏰ Timestamp and node information

---

## 🔍 Monitoring Commands

### View All Logs
```bash
docker-compose logs -f
```

### View Specific Service
```bash
# Edge node 1
docker-compose logs -f sensor-edge-1

# Edge node 2
docker-compose logs -f sensor-edge-2

# Dashboard
docker-compose logs -f monitoring-dashboard

# Data logger
docker-compose logs -f data-logger

# MQTT Broker
docker-compose logs -f mqtt-broker
```

### Monitor MQTT Traffic
```bash
# Subscribe to all topics
docker exec -it mqtt-broker mosquitto_sub -t 'env/#' -v

# Subscribe to events only
docker exec -it mqtt-broker mosquitto_sub -t 'env/event/#' -v

# Subscribe to specific sensor
docker exec -it mqtt-broker mosquitto_sub -t 'env/temperature/#' -v
```

### Check Container Status
```bash
docker-compose ps
```

### Check MongoDB Data
```bash
# Access MongoDB shell
docker exec -it db-logger mongosh

# In MongoDB shell:
use sensor_data

# Count documents
db.sensor_readings.countDocuments()
db.events.countDocuments()

# View latest readings
db.sensor_readings.find().sort({logged_at: -1}).limit(10)

# View latest events
db.events.find().sort({logged_at: -1}).limit(10)

# Query specific node
db.sensor_readings.find({node: "edge-1"}).limit(5)

# Query specific sensor
db.sensor_readings.find({sensor: "temperature"}).limit(5)
```

---

## 🛠️ Management Commands

### Stop System
```bash
docker-compose down
```

### Restart System
```bash
docker-compose restart
```

### Restart Specific Service
```bash
docker-compose restart sensor-edge-1
docker-compose restart monitoring-dashboard
```

### Rebuild After Code Changes
```bash
docker-compose up --build -d
```

### Clean Everything (including volumes)
```bash
docker-compose down -v
```

### Scale Edge Nodes
```bash
# Add more edge nodes
docker-compose up -d --scale sensor-edge-1=3
```

---

## 🧪 Testing

### Test MQTT Manually

**Publish test message**:
```bash
docker exec -it mqtt-broker mosquitto_pub \
  -t 'env/temperature/raw' \
  -m '{"sensor":"temperature","value":25.5,"timestamp":"2025-11-29T10:00:00Z","node":"test-node","event":false}'
```

**Publish test event**:
```bash
docker exec -it mqtt-broker mosquitto_pub \
  -t 'env/event/temperature_alert' \
  -m '{"sensor":"temperature","value":35.0,"timestamp":"2025-11-29T10:00:00Z","node":"test-node","event":true,"event_type":"temperature_alert_high"}'
```

### Simulate Node Failure
```bash
# Stop one edge node
docker stop edge-node-1

# System continues working (fault tolerance)
# edge-node-2 keeps sending data

# Restart failed node
docker start edge-node-1

# Node reconnects automatically
```

---

## 📈 Expected Behavior

### Sensor Value Ranges
- **Temperature**: 10-35°C (random)
- **Humidity**: 30-90% (random)
- **Light**: 50-500 lumens (random)
- **Air Quality**: 500-1500 ppm (random)

### Alert Triggers
- **Temperature**: <15°C or >30°C
- **Humidity**: <40% or >80%
- **Light**: <100 lumens
- **Air Quality**: >1000 ppm

### Update Frequencies
- Temperature & Humidity: Every 5 seconds
- Light & Air Quality: Every 10 seconds

---

## 🐛 Troubleshooting

### Problem: Dashboard shows no data

**Solution**:
```bash
# Check if MQTT broker is running
docker ps | grep mqtt-broker

# Check edge node logs
docker-compose logs sensor-edge-1

# Restart dashboard
docker-compose restart monitoring-dashboard
```

### Problem: Container keeps restarting

**Solution**:
```bash
# Check logs for errors
docker-compose logs [service-name]

# Common issues:
# - MQTT broker not ready → wait 10 seconds
# - MongoDB not ready → wait 10 seconds
# - Port already in use → stop conflicting service
```

### Problem: Port already in use

**Solution**:
```bash
# Check what's using the port
sudo lsof -i :3000  # Dashboard
sudo lsof -i :1883  # MQTT

# Kill the process or change port in docker-compose.yml
```

### Problem: Cannot connect to MQTT broker

**Solution**:
```bash
# Ensure broker is running
docker exec -it mqtt-broker mosquitto -h

# Test connection
docker exec -it mqtt-broker mosquitto_sub -t '$$SYS/#' -C 1

# Restart broker
docker-compose restart mqtt-broker
```

---

## 📚 Architecture Summary

```
Flow: Sensor → Edge Compute → MQTT → Dashboard
      ────────────────────────────────────────
      1. Read sensor value (thread)
      2. Check constraint (local)
      3. Publish MQTT message
      4. Broker distributes
      5. Dashboard receives
      6. Update UI in real-time
      7. Logger saves to DB
```

**Key Concepts Demonstrated**:
- ✅ Message Passing (MQTT)
- ✅ No Shared Memory
- ✅ Edge Computing
- ✅ Event-Driven
- ✅ Concurrency (threads)
- ✅ Distributed Processes
- ✅ Loose Coupling
- ✅ Scalability

---

## 🎯 Success Criteria

Your system is working correctly if:
- ✅ Dashboard shows 4 graphs updating in real-time
- ✅ Data from both edge-1 and edge-2 appears
- ✅ Alerts appear when values violate constraints
- ✅ MQTT broker shows connected clients
- ✅ MongoDB accumulates data
- ✅ Logs show sensor readings every 5-10 seconds

---

## 💡 Tips

1. **Keep terminal open** to see real-time logs
2. **Open multiple terminals** for different services
3. **Use Ctrl+C** to stop following logs
4. **Refresh browser** if dashboard doesn't update
5. **Check network** with `docker network ls`

---

## 🚀 Next Steps

After getting familiar with the basic system:

1. **Add custom constraints** in `edge/sensor_edge.py`
2. **Modify sensor intervals** to see different update patterns
3. **Add new edge nodes** to test scalability
4. **Customize dashboard UI** in `dashboard/public/index.html`
5. **Implement new sensors** (e.g., pressure, CO2)
6. **Add authentication** to MQTT broker
7. **Deploy to cloud** (AWS, Azure, GCP)

---

**Happy Monitoring! 🌍📊**
