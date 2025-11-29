# 🌿 Greenhouse Environmental Monitoring System - Sistem Terdistribusi Lengkap

## 📋 Deskripsi Proyek

Proyek ini adalah implementasi lengkap **Greenhouse Environmental Monitoring System** berbasis **sistem terdistribusi (distributed system)** yang menerapkan konsep-konsep fundamental:

- ✅ **Message Passing** via MQTT (bukan shared memory)
- ✅ **Edge Computing** dengan komputasi lokal pada node sensor
- ✅ **Event-Driven Architecture** untuk trigger alert otomatis
- ✅ **Loose Coupling** antar service/container
- ✅ **Concurrency** dengan multi-threading
- ✅ **Scalability** mendukung multiple edge nodes
- ✅ **Autonomous Processes** setiap service berjalan mandiri

---

## 🏗️ Arsitektur Sistem Terdistribusi

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTED SYSTEM ARCHITECTURE                   │
│                    (Message Passing - No Shared Memory)              │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐         ┌──────────────────┐
    │  Edge Node 1     │         │  Edge Node 2     │
    │  (Container)     │         │  (Container)     │
    ├──────────────────┤         ├──────────────────┤
    │ • 4 Sensor       │         │ • 4 Sensor       │
    │   Threads        │         │   Threads        │
    │ • Concurrent     │         │ • Concurrent     │
    │ • Edge Compute   │         │ • Edge Compute   │
    │ • Constraint     │         │ • Constraint     │
    │   Checking       │         │   Checking       │
    └────────┬─────────┘         └────────┬─────────┘
             │                            │
             │ PUBLISH (MQTT)             │ PUBLISH (MQTT)
             │ env/*/raw                  │ env/*/raw
             │ env/event/*                │ env/event/*
             │                            │
             └────────────┬───────────────┘
                          ↓
              ┌───────────────────────┐
              │   MQTT Broker         │
              │   (Mosquitto)         │
              ├───────────────────────┤
              │ • Message Passing Hub │
              │ • Publish/Subscribe   │
              │ • Decoupling Layer    │
              └───────────┬───────────┘
                          │
                          │ SUBSCRIBE (MQTT)
                          │ env/#
                          │
           ┌──────────────┼──────────────┐
           ↓              ↓              ↓
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │Dashboard │   │  Data    │   │  Other   │
    │(Node.js) │   │  Logger  │   │ Services │
    ├──────────┤   ├──────────┤   ├──────────┤
    │• Web UI  │   │• MongoDB │   │• Future  │
    │• Real-   │   │• Persist │   │  Nodes   │
    │  time    │   │  Data    │   │          │
    │  Graph   │   │          │   │          │
    │• Alerts  │   │          │   │          │
    └──────────┘   └──────────┘   └──────────┘
```

### Prinsip Sistem Terdistribusi yang Diterapkan

1. **No Shared Memory**
   - Setiap container memiliki memory space sendiri
   - Tidak ada akses langsung ke memory container lain
   - Komunikasi HANYA via message passing (MQTT)

2. **Message Passing Architecture**
   - MQTT sebagai protokol komunikasi
   - Publish-Subscribe pattern
   - Asynchronous message delivery
   - Decoupling producer dan consumer

3. **Autonomous Processes**
   - Setiap service berjalan sebagai proses independen
   - Dapat di-restart tanpa mempengaruhi service lain
   - Scalable: dapat menambahkan node baru dengan mudah

4. **Concurrency**
   - Edge node menjalankan 4 thread sensor secara concurrent
   - Thread-safe message publishing
   - Non-blocking I/O operations

5. **Event-Driven Mechanism**
   - Trigger otomatis saat constraint dilanggar
   - Real-time event notification
   - Reactive system behavior

---

## 🔧 Komponen Sistem

### 1. **MQTT Broker** (Eclipse Mosquitto)
- **Fungsi**: Central message passing hub
- **Port**: 1883 (MQTT), 9001 (WebSocket)
- **Peran**: Menjembatani komunikasi antar semua service

### 2. **Edge Node Service** (Python)
- **Fungsi**: Edge computing untuk sensor monitoring
- **Teknologi**: Python + Threading + MQTT
- **Fitur**:
  - 4 sensor threads concurrent (temperature, humidity, light, air quality)
  - Local constraint checking (edge computing)
  - Event-driven alert generation
  - MQTT publisher

**Constraint Rules (Edge Computing)**:
```python
temperature: >30°C atau <15°C   → ALERT
humidity: <40% atau >80%        → ALERT
light: <100 lumens              → ALERT
airquality: >1000 ppm           → WARNING
```

**Thread Intervals**:
- Temperature: 5 detik
- Humidity: 5 detik
- Light: 10 detik
- Air Quality: 10 detik

### 3. **Monitoring Dashboard** (Node.js + Express + Socket.IO)
- **Fungsi**: Real-time visualization & control
- **Port**: 3000
- **Fitur**:
  - ✅ **4 grafik time-series real-time** dengan Chart.js
  - ✅ **Time range selector** (5 min / 15 min / 1 hour)
  - ✅ **Smart Control Panel** dengan rekomendasi aksi otomatis
  - ✅ **Simulation Controls** untuk testing (overheat, low light, poor air)
  - ✅ **Real-time Event Alert Panel** dengan detail lengkap
  - ✅ **10 Recent Updates Panel** untuk tracking data terbaru
  - ✅ Multi-node support dengan color coding
  - ✅ WebSocket untuk push data ke client
  - ✅ Responsive design untuk mobile & desktop

### 4. **Data Logger** (Python + MongoDB)
- **Fungsi**: Persistence layer
- **Teknologi**: Python + PyMongo
- **Fitur**:
  - Subscribe semua topic MQTT
  - Simpan ke MongoDB
  - Separate collections untuk data & events

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW SEQUENCE                           │
└─────────────────────────────────────────────────────────────────────┘

STEP 1: Edge Computing (Local Processing)
─────────────────────────────────────────
┌───────────────┐
│ Sensor Thread │ → Read Value (e.g., temp=32°C)
└───────┬───────┘
        ↓
┌───────────────────┐
│ Constraint Check  │ → if temp > 30°C → EVENT = True
└───────┬───────────┘
        ↓
┌───────────────────┐
│ Generate Payload  │ → {sensor, value, timestamp, node, event}
└───────┬───────────┘
        ↓

STEP 2: Message Passing (MQTT Publish)
───────────────────────────────────────
┌─────────────────────────────────┐
│ MQTT Publish                    │
├─────────────────────────────────┤
│ • Topic: env/temperature/raw    │  ← Normal data
│ • Topic: env/event/temp_alert   │  ← Event data
│ • Payload: JSON                 │
└───────────┬─────────────────────┘
            ↓
        [ MQTT BROKER ]
            ↓

STEP 3: Message Distribution (Pub-Sub)
───────────────────────────────────────
        ┌───────┬───────┐
        ↓       ↓       ↓
    [Dashboard] [Logger] [Other Subscribers]
        ↓
STEP 4: Real-time Visualization
────────────────────────────────
    • Update chart
    • Show alert
    • WebSocket → Browser
```

---

## 🚀 Cara Menjalankan

### Prerequisites
- Docker
- Docker Compose

### Langkah-langkah

1. **Clone/Download project**
   ```bash
   cd mqtt-env-monitoring
   ```

2. **Build dan start semua container**
   ```bash
   docker-compose up --build
   ```

3. **Akses dashboard**
   ```
   http://localhost:3000
   ```

4. **Monitor logs**
   ```bash
   # Lihat log edge node
   docker logs -f edge-node-1
   
   # Lihat log dashboard
   docker logs -f monitoring-dashboard
   
   # Lihat log data logger
   docker logs -f data-logger
   ```

5. **Stop sistem**
   ```bash
   docker-compose down
   ```

---

## 📁 Struktur Folder

```
mqtt-env-monitoring/
├── docker-compose.yml           # Orchestration file
├── README.md                    # Documentation
│
├── broker/                      # MQTT Broker config
│   └── mosquitto.conf
│
├── edge/                        # Edge Computing Node
│   ├── Dockerfile
│   ├── requirements.txt
│   └── sensor_edge.py          # Multi-threaded sensor
│
├── dashboard/                   # Monitoring Dashboard
│   ├── Dockerfile
│   ├── package.json
│   ├── server.js               # Node.js server
│   └── public/
│       └── index.html          # Web UI
│
└── logger/                      # Data Logger Service
    ├── Dockerfile
    ├── requirements.txt
    └── data_logger.py          # MQTT → MongoDB
```

---

## 🔌 MQTT Topics

### Raw Data Channels
```
env/temperature/raw
env/humidity/raw
env/light/raw
env/airquality/raw
```

### Event Channels (Event-Driven)
```
env/event/temperature_alert_high
env/event/temperature_alert_low
env/event/humidity_alert_high
env/event/humidity_alert_low
env/event/light_low
env/event/airquality_warning
```

### Control Channels (Simulation)
```
greenhouse/control/simulate
```
Payload:
```json
{
  "type": "overheat|lowlight|poorair|reset",
  "timestamp": "2025-11-29T10:30:00.000Z"
}
```

### Payload Format
```json
{
  "sensor": "temperature",
  "value": 32.5,
  "timestamp": "2025-11-29T10:30:00.000Z",
  "node": "edge-1",
  "event": true,
  "event_type": "temperature_alert_high"
}
```

---

## 🔄 Scalability

Sistem mendukung penambahan edge node dengan mudah:

```bash
# Edit docker-compose.yml, tambahkan:
sensor-edge-3:
  build: ./edge
  container_name: edge-node-3
  environment:
    - NODE_ID=edge-3
    - MQTT_BROKER=mqtt-broker
    - MQTT_PORT=1883
  depends_on:
    - mqtt-broker
  networks:
    - mqtt-network
```

Dashboard akan otomatis mendeteksi dan menampilkan data dari node baru tanpa perlu konfigurasi tambahan (loose coupling).

---

## 🎯 Konsep Sistem Terdistribusi yang Terpenuhi

✅ **Distributed Processes**: Setiap container = process terpisah  
✅ **Message Passing**: MQTT sebagai communication layer  
✅ **No Shared Memory**: Isolation antar container  
✅ **Concurrency**: Multi-threading pada edge node  
✅ **Asynchronous I/O**: Non-blocking operations  
✅ **Loose Coupling**: Service independen satu sama lain  
✅ **Event-Driven**: Reactive architecture  
✅ **Scalability**: Support multiple nodes  
✅ **Fault Tolerance**: Service dapat restart independen  
✅ **Location Transparency**: Service tidak perlu tahu lokasi fisik service lain  

---

## 📈 Monitoring & Testing

### Test MQTT manually
```bash
# Subscribe ke semua topics
docker exec -it mqtt-broker mosquitto_sub -t 'env/#' -v

# Publish manual test
docker exec -it mqtt-broker mosquitto_pub -t 'env/test' -m '{"test": true}'
```

### Check MongoDB data
```bash
# Akses MongoDB
docker exec -it db-logger mongosh

# Query data
use sensor_data
db.sensor_readings.find().limit(5)
db.events.find().limit(5)
```

---

## 🛠️ Troubleshooting

### Container tidak bisa connect ke MQTT
- Pastikan mqtt-broker sudah running
- Cek network: `docker network inspect mqtt-env-monitoring_mqtt-network`

### Dashboard tidak tampil data
- Cek logs dashboard: `docker logs monitoring-dashboard`
- Pastikan browser bisa akses WebSocket

### Edge node error
- Cek logs: `docker logs edge-node-1`
- Pastikan MQTT broker accessible

---

## 📚 Referensi Teknologi

- **MQTT**: [https://mqtt.org/](https://mqtt.org/)
- **Docker Compose**: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **Eclipse Mosquitto**: [https://mosquitto.org/](https://mosquitto.org/)
- **Paho MQTT Python**: [https://pypi.org/project/paho-mqtt/](https://pypi.org/project/paho-mqtt/)
- **Socket.IO**: [https://socket.io/](https://socket.io/)
- **Chart.js**: [https://www.chartjs.org/](https://www.chartjs.org/)

---

## 👨‍💻 Author

Project Sistem Terdistribusi - Monitoring Lingkungan berbasis Edge Computing

---

## 📄 License

MIT License - Free to use for educational purposes

---

## 🎓 Pembelajaran

Project ini mendemonstrasikan:

1. **Distributed System Design Patterns**
   - Publisher-Subscriber pattern
   - Message-oriented middleware
   - Event-driven architecture

2. **Edge Computing Concepts**
   - Local data processing
   - Constraint checking at edge
   - Reduce latency & bandwidth

3. **Concurrency & Parallelism**
   - Multi-threading
   - Thread-safe operations
   - Concurrent data streams

4. **Microservices Architecture**
   - Service isolation
   - Container orchestration
   - Independent deployment

---

**Happy Distributed Computing! 🚀**
