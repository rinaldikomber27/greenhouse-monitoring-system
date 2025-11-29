# 🧪 Testing Guide - Distributed System Principles

## Cara Test 2 Node Sesuai Kaidah Sistem Terdistribusi

Panduan ini menunjukkan cara membuktikan bahwa sistem benar-benar terdistribusi dan memenuhi prinsip-prinsip distributed systems.

---

## 1️⃣ TEST: MESSAGE PASSING (No Shared Memory)

### Prinsip yang Diuji:
✅ Setiap node berkomunikasi via MQTT (message passing)  
✅ Tidak ada shared memory antar container  
✅ Data dikirim sebagai message, bukan akses memori langsung

### Cara Test:

#### A. Monitor MQTT Traffic Real-time
```bash
# Terminal 1: Subscribe ke semua MQTT messages
docker exec -it mqtt-broker mosquitto_sub -t 'env/#' -v
```

**Yang Harus Terlihat:**
```
env/temperature/raw {"sensor":"temperature","value":25.5,"node":"edge-1",...}
env/temperature/raw {"sensor":"temperature","value":24.8,"node":"edge-2",...}
env/humidity/raw {"sensor":"humidity","value":65.3,"node":"edge-1",...}
```

✅ **PASS jika:** Anda melihat message dari edge-1 DAN edge-2 bergantian via MQTT broker

#### B. Inspect Network Isolation
```bash
# Cek bahwa container tidak bisa akses memory satu sama lain
docker exec edge-node-1 ps aux
docker exec edge-node-2 ps aux

# Cek namespace isolation
docker exec edge-node-1 cat /proc/1/cgroup
docker exec edge-node-2 cat /proc/1/cgroup
```

✅ **PASS jika:** Setiap container memiliki process ID space terpisah (PID 1 berbeda)

---

## 2️⃣ TEST: DISTRIBUTED AUTONOMY (Independent Operation)

### Prinsip yang Diuji:
✅ Setiap node beroperasi secara independen  
✅ Node tidak bergantung pada node lain  
✅ Failure di satu node tidak crash sistem

### Cara Test:

#### A. Stop Edge Node 1
```bash
# Terminal 1: Monitor dashboard logs
docker logs -f monitoring-dashboard

# Terminal 2: Stop edge-node-1
docker stop edge-node-1
```

**Yang Harus Terlihat di Dashboard:**
- ✅ Data dari edge-2 TETAP mengalir
- ✅ Grafik edge-2 terus update
- ✅ Sistem tidak crash
- ✅ Alert dari edge-2 tetap muncul

#### B. Restart Edge Node 1
```bash
# Restart node yang di-stop
docker start edge-node-1

# Tunggu 10 detik, lalu cek log
docker logs edge-node-1 --tail 20
```

**Yang Harus Terlihat:**
- ✅ Edge-1 reconnect ke MQTT broker otomatis
- ✅ Edge-1 mulai kirim data lagi
- ✅ Dashboard otomatis detect edge-1 aktif kembali
- ✅ Grafik menampilkan 2 garis lagi

#### C. Test: Stop dan Start Bergantian
```bash
# Stop edge-1, tunggu 30 detik
docker stop edge-node-1
sleep 30

# Stop edge-2, start edge-1
docker stop edge-node-2
docker start edge-node-1
sleep 30

# Start edge-2
docker start edge-node-2
```

✅ **PASS jika:** Sistem tetap berjalan dengan minimal 1 node aktif

---

## 3️⃣ TEST: LOOSE COUPLING (Service Independence)

### Prinsip yang Diuji:
✅ Service tidak tahu implementasi service lain  
✅ Komunikasi hanya via interface (MQTT topics)  
✅ Dapat restart/update service tanpa affect lainnya

### Cara Test:

#### A. Restart Dashboard (Service Lain Tetap Jalan)
```bash
# Monitor edge nodes tetap jalan
docker logs -f edge-node-1 &
docker logs -f edge-node-2 &

# Restart dashboard
docker-compose restart monitoring-dashboard

# Cek edge nodes
fg  # Lihat logs edge nodes masih jalan
```

✅ **PASS jika:** Edge nodes tidak terpengaruh restart dashboard

#### B. Restart MQTT Broker (Reconnect Otomatis)
```bash
# Terminal 1: Monitor edge node logs
docker logs -f edge-node-1

# Terminal 2: Restart broker
docker-compose restart mqtt-broker

# Tunggu 5 detik
```

**Yang Harus Terlihat di Edge Node Log:**
```
[edge-1] Connection lost...
[edge-1] Reconnecting to MQTT Broker...
[edge-1] Connected to MQTT Broker (Message Passing Hub)
[edge-1] MQTT connection established
```

✅ **PASS jika:** Edge nodes auto-reconnect tanpa manual intervention

#### C. Test: Add Third Edge Node
```bash
# Edit docker-compose.yml, tambahkan:
sensor-edge-3:
  build: ./edge
  container_name: edge-node-3
  environment:
    - MQTT_BROKER=mqtt-broker
    - MQTT_PORT=1883
    - NODE_ID=edge-3
  depends_on:
    - mqtt-broker
  networks:
    - mqtt-network

# Start node baru
docker-compose up -d sensor-edge-3

# Cek dashboard
curl http://localhost:3000
```

✅ **PASS jika:** Dashboard otomatis detect edge-3 tanpa code changes

---

## 4️⃣ TEST: CONCURRENCY (Multi-Threading)

### Prinsip yang Diuji:
✅ Multiple threads berjalan concurrent di setiap node  
✅ Thread-safe operations  
✅ Parallel sensor reading

### Cara Test:

#### A. Monitor Thread Activity
```bash
# Cek thread count di edge node
docker exec edge-node-1 ps -T | grep python

# Atau lihat log startup
docker logs edge-node-1 | grep "Thread started"
```

**Yang Harus Terlihat:**
```
Thread started for temperature sensor (interval: 20s)
Thread started for humidity sensor (interval: 20s)
Thread started for light sensor (interval: 20s)
Thread started for airquality sensor (interval: 20s)
All 4 sensor threads running concurrently
```

✅ **PASS jika:** Melihat 4 thread berjalan concurrent per node

#### B. Verify Concurrent Publishing
```bash
# Subscribe dengan timestamp
docker exec -it mqtt-broker mosquitto_sub -t 'env/+/raw' -v | while read line; do echo "[$(date +%H:%M:%S)] $line"; done
```

**Yang Harus Terlihat:**
```
[10:30:15] env/temperature/raw {...}
[10:30:15] env/humidity/raw {...}
[10:30:16] env/light/raw {...}
[10:30:16] env/airquality/raw {...}
```

✅ **PASS jika:** Data dari berbagai sensor datang hampir bersamaan (concurrent)

---

## 5️⃣ TEST: EVENT-DRIVEN ARCHITECTURE

### Prinsip yang Diuji:
✅ System react to events (bukan polling)  
✅ Event trigger di edge node  
✅ Event propagation ke subscribers

### Cara Test:

#### A. Trigger Event Simulation
```bash
# Terminal 1: Subscribe ke event topics
docker exec -it mqtt-broker mosquitto_sub -t 'env/event/#' -v

# Terminal 2: Buka dashboard di browser
# http://localhost:3000

# Terminal 3: Trigger simulation
# Di browser, klik button "🔥 Simulate Overheat"
```

**Flow yang Harus Terjadi:**
1. Browser → WebSocket → Dashboard Server
2. Dashboard → MQTT publish → `greenhouse/control/simulate`
3. Edge Nodes subscribe → Receive command
4. Edge Nodes modify sensor behavior
5. Edge Nodes detect violation → Publish event
6. Dashboard subscribe → Show alert

✅ **PASS jika:** Event muncul dalam 20-30 detik setelah simulasi

#### B. Natural Event Test
```bash
# Monitor untuk event alami (tanpa simulasi)
docker logs -f edge-node-1 | grep "EVENT TRIGGERED"
```

**Tunggu hingga melihat:**
```
[edge-1] 🚨 EVENT TRIGGERED: temperature_alert_high | Value: 32.5
[edge-1] 🚨 EVENT TRIGGERED: airquality_warning | Value: 1150.3
```

✅ **PASS jika:** Alert muncul di dashboard secara real-time

---

## 6️⃣ TEST: EDGE COMPUTING (Local Processing)

### Prinsip yang Diuji:
✅ Constraint checking dilakukan di edge (bukan central)  
✅ Reduce bandwidth - hanya kirim filtered data  
✅ Local decision making

### Cara Test:

#### A. Verify Edge Computation
```bash
# Monitor edge node logs untuk lihat constraint checking
docker logs -f edge-node-1

# Cari pattern:
# "📊 Normal reading:" = constraint passed
# "🚨 EVENT TRIGGERED:" = constraint violated
```

**Yang Harus Terlihat:**
- Edge node melakukan check_constraint SEBELUM publish
- Bukan central server yang check
- Decision dibuat lokal

#### B. Compare Raw vs Event Data
```bash
# Terminal 1: Count raw messages
docker exec -it mqtt-broker mosquitto_sub -t 'env/+/raw' -C 100 | wc -l

# Terminal 2: Count event messages
docker exec -it mqtt-broker mosquitto_sub -t 'env/event/#' -C 100 | wc -l
```

✅ **PASS jika:** Event messages JAUH LEBIH SEDIKIT dari raw messages (filtering works)

---

## 7️⃣ TEST: SCALABILITY (Horizontal Scaling)

### Prinsip yang Diuji:
✅ Dapat menambah node tanpa code changes  
✅ Load distribution  
✅ System handles multiple nodes gracefully

### Cara Test:

#### A. Add Multiple Nodes
```bash
# Scale edge nodes
docker-compose up -d --scale sensor-edge-1=3

# Atau tambah manual
docker run -d \
  --name edge-node-4 \
  --network mqtt-env-monitoring_mqtt-network \
  -e NODE_ID=edge-4 \
  -e MQTT_BROKER=mqtt-broker \
  mqtt-env-monitoring-sensor-edge-1
```

#### B. Verify Dashboard Auto-Detection
```bash
# Akses dashboard
curl http://localhost:3000

# Cek status bar "Greenhouse Zones" counter
# Harus otomatis increment
```

✅ **PASS jika:** Dashboard detect semua nodes tanpa configuration changes

---

## 8️⃣ TEST: BIDIRECTIONAL COMMUNICATION

### Prinsip yang Diuji:
✅ Data flow: Edge → Dashboard (monitoring)  
✅ Control flow: Dashboard → Edge (command)  
✅ Two-way MQTT communication

### Cara Test:

#### A. Send Control Command
```bash
# Terminal 1: Monitor edge node
docker logs -f edge-node-1 | grep "simulation"

# Terminal 2: Publish manual command
docker exec -it mqtt-broker mosquitto_pub \
  -t 'greenhouse/control/simulate' \
  -m '{"type":"overheat","timestamp":"2025-11-29T10:00:00Z"}'

# Atau via dashboard button
```

**Yang Harus Terlihat:**
```
[edge-1] Received simulation command: overheat
[edge-1] 🚨 EVENT TRIGGERED: temperature_alert_high | Value: 34.5
```

✅ **PASS jika:** Edge nodes respond to control commands

---

## 9️⃣ TEST: FAULT TOLERANCE

### Prinsip yang Diuji:
✅ System toleran terhadap failure  
✅ Graceful degradation  
✅ Auto-recovery

### Cara Test:

#### A. Kill Random Node
```bash
# Simulate crash
docker kill edge-node-1

# Monitor system
watch -n 1 'docker-compose ps'

# Cek dashboard tetap jalan
curl http://localhost:3000
```

✅ **PASS jika:** System tetap operational dengan node yang tersisa

#### B. Network Partition Simulation
```bash
# Disconnect node dari network
docker network disconnect mqtt-env-monitoring_mqtt-network edge-node-1

# Tunggu 30 detik

# Reconnect
docker network connect mqtt-env-monitoring_mqtt-network edge-node-1
docker restart edge-node-1
```

✅ **PASS jika:** Node auto-reconnect dan resume operation

---

## 🔟 TEST: LOCATION TRANSPARENCY

### Prinsip yang Diuji:
✅ Service tidak perlu tahu lokasi fisik service lain  
✅ Communication via logical names (hostname)  
✅ Deploy anywhere, works the same

### Cara Test:

#### A. Inspect Container Communication
```bash
# Edge node tidak tahu IP address dashboard
docker exec edge-node-1 cat sensor_edge.py | grep -i "dashboard\|3000\|localhost"

# Hanya tahu MQTT broker hostname
docker exec edge-node-1 env | grep MQTT_BROKER
```

✅ **PASS jika:** Services only know logical hostnames, not IP addresses

---

## 📊 COMPREHENSIVE TEST SCRIPT

Jalankan semua test otomatis:

```bash
#!/bin/bash
# File: test_distributed_system.sh

echo "🧪 DISTRIBUTED SYSTEM PRINCIPLES TEST"
echo "======================================"

# Test 1: Message Passing
echo "1. Testing Message Passing..."
timeout 5 docker exec mqtt-broker mosquitto_sub -t 'env/#' -C 10 > /dev/null && echo "✅ PASS" || echo "❌ FAIL"

# Test 2: Independent Nodes
echo "2. Testing Node Independence..."
docker stop edge-node-1
sleep 5
docker logs edge-node-2 --tail 5 | grep -q "Normal reading" && echo "✅ PASS" || echo "❌ FAIL"
docker start edge-node-1

# Test 3: Concurrency
echo "3. Testing Concurrency..."
docker logs edge-node-1 | grep -q "4 sensor threads running concurrently" && echo "✅ PASS" || echo "❌ FAIL"

# Test 4: Event-Driven
echo "4. Testing Event-Driven..."
docker logs edge-node-1 | grep -q "EVENT TRIGGERED" && echo "✅ PASS" || echo "❌ FAIL"

# Test 5: Auto-Reconnect
echo "5. Testing Fault Tolerance..."
docker restart mqtt-broker
sleep 10
docker logs edge-node-1 --tail 10 | grep -q "Connected to MQTT" && echo "✅ PASS" || echo "❌ FAIL"

echo "======================================"
echo "✅ Distributed System Test Complete!"
```

---

## 📝 CHECKLIST AKHIR

Sistem memenuhi kaidah distributed system jika:

- [ ] ✅ Komunikasi via message passing (MQTT)
- [ ] ✅ No shared memory between containers
- [ ] ✅ Nodes operate independently (autonomous)
- [ ] ✅ Loose coupling (service isolation)
- [ ] ✅ Concurrent operations (multi-threading)
- [ ] ✅ Event-driven reactions
- [ ] ✅ Edge computing (local processing)
- [ ] ✅ Scalable (add nodes easily)
- [ ] ✅ Fault tolerant (survive failures)
- [ ] ✅ Location transparency
- [ ] ✅ Bidirectional communication

---

## 🎯 DEMO SCENARIO LENGKAP

**Scenario: Greenhouse Monitoring dengan Node Failure**

```bash
# 1. Start sistem
docker-compose up -d

# 2. Buka dashboard
firefox http://localhost:3000 &

# 3. Monitor MQTT traffic
docker exec -it mqtt-broker mosquitto_sub -t 'env/#' -v &

# 4. Lihat data dari 2 nodes mengalir
# Tunggu 1 menit

# 5. Simulate node failure
docker stop edge-node-1

# 6. Verifikasi:
# - Dashboard tetap update dari edge-2 ✅
# - Grafik edge-1 berhenti, edge-2 lanjut ✅
# - System tidak crash ✅

# 7. Recover node
docker start edge-node-1

# 8. Verifikasi:
# - Edge-1 auto-reconnect ✅
# - Dashboard detect edge-1 kembali ✅
# - 2 garis muncul lagi di grafik ✅

# 9. Test simulasi
# Klik button "Simulate Overheat" di dashboard

# 10. Verifikasi:
# - Command propagate ke SEMUA nodes ✅
# - Edge-1 dan edge-2 trigger alerts ✅
# - Dashboard show alerts dari kedua nodes ✅
```

---

**🎉 Dengan mengikuti test di atas, Anda membuktikan sistem benar-benar distributed!**
