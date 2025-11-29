# 🎮 Greenhouse Dashboard - User Guide

## Fitur Dashboard Lengkap

Dashboard Greenhouse Environmental Monitoring System dilengkapi dengan berbagai fitur interaktif untuk monitoring dan kontrol sistem terdistribusi secara real-time.

---

## 📊 1. Historical Time-Series Graphs

### Grafik Real-Time dengan Chart.js

Dashboard menampilkan **4 grafik time-series** yang terus diperbarui:

- 🌡️ **Temperature (°C)** - Suhu greenhouse per zona
- 💧 **Humidity (%)** - Kelembaban udara per zona
- 💡 **Light (lumens)** - Intensitas cahaya per zona
- 🌫️ **Air Quality (ppm)** - Kualitas udara per zona

### Fitur Grafik:
- ✅ **Multi-node comparison** - Membandingkan data dari edge-1 dan edge-2
- ✅ **Color-coded lines** - Setiap node memiliki warna berbeda
- ✅ **Smooth animation** - Update grafik tanpa lag
- ✅ **Auto-scaling Y-axis** - Menyesuaikan range nilai otomatis
- ✅ **Time-based X-axis** - Format waktu HH:mm

---

## ⏱️ 2. Time Range Selector

Pilih rentang waktu untuk melihat data historis:

- **5 Minutes** - Data 5 menit terakhir (update cepat, detail tinggi)
- **15 Minutes** ⭐ - Data 15 menit terakhir (default, balanced)
- **1 Hour** - Data 1 jam terakhir (overview jangka panjang)

### Cara Kerja:
1. Klik salah satu tombol time range
2. Semua 4 grafik akan otomatis filter data sesuai rentang waktu
3. Data disimpan dalam buffer RAM untuk akses cepat
4. Grafik tetap update real-time sesuai data baru yang masuk

---

## 🎮 3. Smart Control & Automation Panel

### Action Cards per Sensor

Dashboard menampilkan **rekomendasi aksi otomatis** untuk setiap jenis alert:

#### 🌡️ Temperature Alert Actions
- ✓ Activate ventilation system
- ✓ Enable misting system  
- ✓ Adjust shade curtains

#### 💧 Humidity Alert Actions
- ✓ Activate humidifier
- ✓ Enable sprinkler system
- ✓ Adjust air circulation

#### 💡 Light Alert Actions
- ✓ Enable LED grow lights
- ✓ Adjust light spectrum
- ✓ Optimize placement

#### 🌫️ Air Quality Alert Actions
- ✓ Open roof ventilation
- ✓ Activate air circulation
- ✓ Enable CO2 regulation

---

## ⚡ 4. Simulation Controls

Dashboard menyediakan **tombol simulasi** untuk testing sistem:

### Tombol Simulasi:

#### 🔥 Simulate Overheat
- Trigger: Paksa sensor temperature membaca nilai tinggi (32-36°C)
- Result: Temperature alert akan muncul
- Use case: Testing sistem ventilasi dan misting

#### 🌙 Simulate Low Light
- Trigger: Paksa sensor light membaca nilai rendah (30-80 lumens)
- Result: Light low warning akan muncul
- Use case: Testing sistem LED grow lights

#### 💨 Simulate Poor Air Quality
- Trigger: Paksa sensor air quality membaca nilai tinggi (1100-1400 ppm)
- Result: Air quality warning akan muncul
- Use case: Testing sistem ventilasi dan sirkulasi udara

#### 🔄 Reset to Normal
- Trigger: Kembalikan semua sensor ke mode normal
- Result: Simulasi berhenti, data kembali normal
- Use case: Menghentikan testing

### Cara Kerja Simulasi:
1. User klik tombol simulasi di dashboard
2. Dashboard kirim command via **WebSocket** ke server
3. Server publish command ke **MQTT topic** `greenhouse/control/simulate`
4. Semua edge nodes **subscribe** ke topic tersebut
5. Edge nodes terima command dan ubah behavior sensor sesuai simulasi
6. Data yang dipublish ke MQTT akan sesuai kondisi simulasi
7. Dashboard terima data simulasi dan tampilkan alert/grafik

**Arsitektur**: Distributed command propagation via message passing (MQTT)

---

## 🚨 5. Real-Time Event Alert Panel

### Fitur Alert Panel:

- **Auto-scrolling list** - 10 alert terbaru
- **Color-coded alerts**:
  - 🔴 **Red (Critical)** - Temperature/humidity alert
  - 🟡 **Yellow (Warning)** - Light low, air quality warning
- **Detailed information**:
  - ⏰ Timestamp (waktu alert trigger)
  - 🚨 Event type (jenis alert)
  - 📊 Sensor name & value
  - 📍 Node location (edge-1 / edge-2)
  - 💡 **Recommended action** (rekomendasi aksi)

### Contoh Alert:

```
⏰ 10:30:15
🚨 TEMPERATURE ALERT HIGH
📊 Sensor: temperature | Value: 32.5
📍 Location: edge-1
💡 Recommended Action: Activate ventilation system and enable misting
```

### Event-Driven Flow:
1. Edge node deteksi constraint violation
2. Publish ke MQTT topic `env/event/[event_type]`
3. Dashboard subscribe dan terima event
4. Tampilkan alert di panel dengan animation (slide-in)
5. Increment counter "Active Alerts"

---

## 📋 6. Recent Updates Panel

### 10 Recent Updates

Panel ini menampilkan **10 aktivitas terbaru** dari sistem:

### Jenis Update:

#### Normal Data Update
```
10:30:15
temperature: 25.3 from edge-1
```

#### Event Update (dengan highlight)
```
10:30:20
🚨 EVENT: TEMPERATURE ALERT HIGH
Sensor: temperature | Value: 32.5 | Node: edge-1
→ Activate ventilation system and enable misting
```

### Fitur:
- ✅ Auto-refresh setiap ada data baru
- ✅ Highlight untuk event (background kuning)
- ✅ Rekomendasi aksi untuk setiap event
- ✅ Scroll untuk lihat history

---

## 📈 7. Status Bar

Status bar di bagian atas menampilkan metrics real-time:

- **📡 MQTT Broker** - Status koneksi (Connected/Disconnected)
- **🌱 Greenhouse Zones** - Jumlah edge nodes aktif
- **📊 Data Points** - Total data points yang diterima
- **🚨 Active Alerts** - Jumlah alert yang sudah trigger

---

## 🎯 Workflow Pengguna

### Scenario 1: Normal Monitoring
1. Buka dashboard `http://localhost:3000`
2. Lihat 4 grafik update real-time setiap 5-10 detik
3. Pilih time range sesuai kebutuhan (5 min / 15 min / 1 hour)
4. Monitor status bar untuk overview sistem
5. Cek Recent Updates untuk aktivitas terbaru

### Scenario 2: Testing Alert System
1. Klik tombol "🔥 Simulate Overheat"
2. Tunggu 5 detik (interval sensor temperature)
3. Lihat alert muncul di Alert Panel
4. Lihat grafik temperature menunjukkan spike
5. Baca rekomendasi aksi di alert
6. Klik "🔄 Reset to Normal" untuk menghentikan simulasi

### Scenario 3: Historical Analysis
1. Pilih time range "1 Hour"
2. Analisis trend data 1 jam terakhir
3. Bandingkan performa edge-1 vs edge-2
4. Identifikasi pola anomali
5. Export data dari MongoDB jika perlu analisis lebih lanjut

---

## 🔌 Technical Implementation

### Technology Stack:
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js 4.4.0 + date adapter
- **Real-time**: Socket.IO (WebSocket)
- **Backend**: Node.js + Express
- **Message Broker**: MQTT (Eclipse Mosquitto)

### Data Flow:
```
Edge Node → MQTT Broker → Dashboard Server → WebSocket → Browser
```

### Real-time Updates:
- WebSocket connection untuk push data tanpa polling
- Chart update menggunakan `chart.update('none')` untuk smooth animation
- DOM manipulation untuk alert panel dan recent updates

---

## 🎨 UI/UX Design Principles

1. **Green Theme** - Mencerminkan greenhouse/lingkungan
2. **Card-based Layout** - Modular dan responsive
3. **Color Coding** - Visual distinction untuk alert severity
4. **Animation** - Smooth slide-in untuk new alerts
5. **Responsive** - Support desktop dan mobile
6. **Accessibility** - Clear labels dan contrast ratio

---

## 🚀 Performance Optimization

- **Time-based data cleanup** - Buffer dibersihkan otomatis untuk hemat RAM
- **Chart animation disabled** untuk real-time update (smooth FPS)
- **Lazy rendering** - Hanya render 10 recent items
- **WebSocket** - Push data, bukan polling (hemat bandwidth)
- **MQTT QoS 0** - Fire-and-forget untuk low latency

---

## 📱 Mobile Support

Dashboard fully responsive untuk akses mobile:
- Grid layout menyesuaikan kolom
- Touch-friendly buttons
- Scrollable alert panel
- Legible charts pada layar kecil

---

**Happy Monitoring! 🌍📊**
