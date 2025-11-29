# 🚀 QUICK REFERENCE CARD

## Greenhouse Environmental Monitoring System

### 📦 Quick Commands

```bash
# START SYSTEM
cd mqtt-env-monitoring
./start.sh
# or
docker-compose up --build -d

# STOP SYSTEM
docker-compose down

# VIEW LOGS
docker-compose logs -f

# VIEW SPECIFIC SERVICE
docker logs -f edge-node-1
docker logs -f monitoring-dashboard

# CHECK STATUS
docker-compose ps

# RESTART SERVICE
docker-compose restart edge-node-1

# REBUILD AFTER CHANGES
docker-compose up --build -d
```

---

### 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Dashboard | http://localhost:3000 | Main monitoring interface |
| MQTT Broker | mqtt://localhost:1883 | MQTT message hub |
| MongoDB | mongodb://localhost:27017 | Data persistence |

---

### 🎮 Dashboard Features Quick Guide

#### 📊 Charts
- **4 real-time graphs** - Temperature, Humidity, Light, Air Quality
- **Multi-node view** - Compare edge-1 vs edge-2
- **Time-series** - Historical data with timestamps

#### ⏱️ Time Range
- **5 Minutes** - Recent detailed view
- **15 Minutes** - Default balanced view
- **1 Hour** - Long-term trend analysis

#### 🎯 Control Panel
- **Temperature Actions** - Ventilation, misting, shading
- **Humidity Actions** - Humidifier, sprinkler, circulation
- **Light Actions** - LED grow lights, spectrum adjustment
- **Air Quality Actions** - Roof ventilation, CO2 regulation

#### ⚡ Simulations
- **🔥 Overheat** - Force high temperature (32-36°C)
- **🌙 Low Light** - Force low light (30-80 lumens)
- **💨 Poor Air** - Force high air quality (1100-1400 ppm)
- **🔄 Reset** - Return to normal operation

#### 🚨 Alerts
- **Real-time panel** - Latest 10 alerts
- **Color-coded** - Red (critical), Yellow (warning)
- **Details** - Timestamp, sensor, value, location
- **Recommendations** - Automated action suggestions

#### 📋 Recent Updates
- **10 latest activities** - Data + events
- **Event highlights** - Yellow background for alerts
- **Full context** - Sensor, value, node, recommendation

---

### 📡 MQTT Topics Reference

#### Data Topics (Raw)
```
env/temperature/raw
env/humidity/raw
env/light/raw
env/airquality/raw
```

#### Event Topics
```
env/event/temperature_alert_high
env/event/temperature_alert_low
env/event/humidity_alert_high
env/event/humidity_alert_low
env/event/light_low
env/event/airquality_warning
```

#### Control Topics
```
greenhouse/control/simulate
```

---

### 🔧 Manual MQTT Testing

```bash
# Subscribe to all topics
docker exec -it mqtt-broker mosquitto_sub -t 'env/#' -v

# Subscribe to events only
docker exec -it mqtt-broker mosquitto_sub -t 'env/event/#' -v

# Publish test message
docker exec -it mqtt-broker mosquitto_pub \
  -t 'env/temperature/raw' \
  -m '{"sensor":"temperature","value":25.5,"timestamp":"2025-11-29T10:00:00Z","node":"test","event":false}'

# Publish test event
docker exec -it mqtt-broker mosquitto_pub \
  -t 'env/event/temperature_alert' \
  -m '{"sensor":"temperature","value":35.0,"timestamp":"2025-11-29T10:00:00Z","node":"test","event":true,"event_type":"temperature_alert_high"}'
```

---

### 💾 MongoDB Quick Access

```bash
# Access MongoDB shell
docker exec -it db-logger mongosh

# In MongoDB shell:
use sensor_data

# Count data
db.sensor_readings.countDocuments()
db.events.countDocuments()

# View latest readings
db.sensor_readings.find().sort({logged_at: -1}).limit(10)

# View latest events
db.events.find().sort({logged_at: -1}).limit(10)

# Query by node
db.sensor_readings.find({node: "edge-1"}).limit(5)

# Query by sensor
db.sensor_readings.find({sensor: "temperature"}).limit(5)
```

---

### 🔍 Troubleshooting Quick Fixes

#### Problem: Dashboard shows no data
```bash
# Check MQTT broker
docker logs mqtt-broker

# Check edge nodes
docker logs edge-node-1

# Restart dashboard
docker-compose restart monitoring-dashboard
```

#### Problem: Container keeps restarting
```bash
# Check logs
docker logs [container-name]

# Common fixes:
# - Wait 10-15 seconds for MQTT broker to be ready
# - Check port conflicts: sudo lsof -i :3000
# - Restart: docker-compose restart [service]
```

#### Problem: Simulation not working
```bash
# Check dashboard server logs
docker logs -f monitoring-dashboard

# Check edge node received command
docker logs -f edge-node-1 | grep "simulation"

# Verify MQTT broker
docker exec -it mqtt-broker mosquitto_sub -t 'greenhouse/control/#' -v
```

---

### 📊 Sensor Constraints Reference

| Sensor | Normal Range | Alert Condition |
|--------|-------------|-----------------|
| Temperature | 15-30°C | <15 or >30 |
| Humidity | 40-80% | <40 or >80 |
| Light | >100 lumens | <100 |
| Air Quality | <1000 ppm | >1000 |

---

### ⏱️ Update Intervals

- **Temperature**: 5 seconds
- **Humidity**: 5 seconds
- **Light**: 10 seconds
- **Air Quality**: 10 seconds

---

### 🎯 Key Files Location

```
mqtt-env-monitoring/
├── docker-compose.yml          # Main orchestration
├── start.sh                    # Quick start script
│
├── edge/sensor_edge.py         # Edge computing logic
├── dashboard/
│   ├── server.js               # Backend server
│   └── public/index.html       # Frontend UI
│
├── README.md                   # Main documentation
├── QUICKSTART.md              # Getting started guide
├── DASHBOARD_GUIDE.md         # Dashboard features
├── ARCHITECTURE_DETAIL.md     # System architecture
└── UPGRADE_SUMMARY.md         # Upgrade changelog
```

---

### 🧪 Testing

```bash
# Run verification test
./test_system.sh

# Expected: 100% pass rate (21/21 tests)
```

---

### 📈 Performance Tips

1. **Time Range**: Use shorter range (5 min) for detailed analysis
2. **Buffer**: System keeps 5 min buffer beyond selected range
3. **Chart Update**: Graphs update smoothly without animation lag
4. **Data Cleanup**: Old data auto-removed to save memory
5. **WebSocket**: Push-based updates (no polling overhead)

---

### 🎓 Architecture Principles

- ✅ **Message Passing** - MQTT pub/sub (no shared memory)
- ✅ **Edge Computing** - Local constraint checking
- ✅ **Event-Driven** - React to threshold violations
- ✅ **Loose Coupling** - Independent services
- ✅ **Concurrency** - Multi-threaded sensors
- ✅ **Scalability** - Add nodes easily
- ✅ **Distributed Control** - Bidirectional MQTT

---

### 📞 Support

- **Documentation**: See README.md, QUICKSTART.md, DASHBOARD_GUIDE.md
- **Architecture**: See ARCHITECTURE_DETAIL.md
- **Changelog**: See UPGRADE_SUMMARY.md

---

**Quick Start: Run `./start.sh` → Open http://localhost:3000 → Test simulations → Monitor alerts! 🚀**
