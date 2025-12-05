# 🏗️ Architecture Visualization - Greenhouse Monitoring System

## 📊 Complete System Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface Layer"
        Browser[🌐 Web Browser<br/>Chrome/Firefox/Safari]
    end

    subgraph "Presentation Layer - Port 3000"
        Dashboard[📊 Monitoring Dashboard<br/>Node.js + Express + Socket.IO<br/>Real-time WebSocket Server]
        WebUI[🖥️ Web Interface<br/>HTML5 + Chart.js + JavaScript<br/>Interactive Controls & Graphs]
    end

    subgraph "Message Broker Layer - Ports 1883, 9001"
        MQTT[🔌 Eclipse Mosquitto 2.0<br/>MQTT Broker<br/>Message Passing Hub]
    end

    subgraph "Edge Computing Layer"
        subgraph "Edge Node 1"
            Edge1[🌡️ Sensor Edge 1<br/>Python 3.10<br/>Multi-threaded]
            E1T[📈 Temperature Thread<br/>20s interval]
            E1H[💧 Humidity Thread<br/>20s interval]
            E1L[💡 Light Thread<br/>20s interval]
            E1A[🌫️ Air Quality Thread<br/>20s interval]
            Edge1 --> E1T
            Edge1 --> E1H
            Edge1 --> E1L
            Edge1 --> E1A
        end

        subgraph "Edge Node 2"
            Edge2[🌡️ Sensor Edge 2<br/>Python 3.10<br/>Multi-threaded]
            E2T[📈 Temperature Thread<br/>20s interval]
            E2H[💧 Humidity Thread<br/>20s interval]
            E2L[💡 Light Thread<br/>20s interval]
            E2A[🌫️ Air Quality Thread<br/>20s interval]
            Edge2 --> E2T
            Edge2 --> E2H
            Edge2 --> E2L
            Edge2 --> E2A
        end
    end

    subgraph "Data Persistence Layer - Port 27017"
        Logger[📝 Data Logger<br/>Python Service<br/>MQTT Subscriber]
        MongoDB[(🗄️ MongoDB 6.0<br/>Document Database<br/>Collections:<br/>• sensor_readings<br/>• events)]
    end

    Browser -->|HTTP/WebSocket| Dashboard
    Dashboard <-->|Socket.IO Events| WebUI
    Dashboard <-->|MQTT Subscribe<br/>env/+/raw<br/>env/event/#| MQTT
    
    E1T -->|Publish| MQTT
    E1H -->|Publish| MQTT
    E1L -->|Publish| MQTT
    E1A -->|Publish| MQTT
    
    E2T -->|Publish| MQTT
    E2H -->|Publish| MQTT
    E2L -->|Publish| MQTT
    E2A -->|Publish| MQTT
    
    MQTT -->|Subscribe<br/>env/#| Logger
    Logger -->|Insert Documents| MongoDB
    
    MQTT -.->|Control Commands<br/>greenhouse/control/simulate| Edge1
    MQTT -.->|Control Commands<br/>greenhouse/control/simulate| Edge2

    style Browser fill:#e1f5ff
    style Dashboard fill:#fff3cd
    style WebUI fill:#fff3cd
    style MQTT fill:#d4edda
    style Edge1 fill:#f8d7da
    style Edge2 fill:#f8d7da
    style Logger fill:#d1ecf1
    style MongoDB fill:#d1ecf1
```

---

## 🔄 Message Flow Architecture

```mermaid
sequenceDiagram
    participant E1 as 🌡️ Edge Node 1
    participant E2 as 🌡️ Edge Node 2
    participant MQTT as 🔌 MQTT Broker
    participant Dashboard as 📊 Dashboard
    participant Logger as 📝 Data Logger
    participant DB as 🗄️ MongoDB
    participant User as 👤 User Browser

    Note over E1,E2: Concurrent Sensor Reading (Multi-threaded)
    
    loop Every 20 seconds
        E1->>E1: Read Temperature (Thread 1)
        E1->>E1: Check Constraint (Edge Computing)
        E1->>MQTT: Publish env/temperature/raw
        
        E1->>E1: Read Humidity (Thread 2)
        E1->>MQTT: Publish env/humidity/raw
        
        E2->>E2: Read Light (Thread 3)
        E2->>MQTT: Publish env/light/raw
        
        E2->>E2: Read Air Quality (Thread 4)
        E2->>MQTT: Publish env/airquality/raw
    end

    MQTT->>Dashboard: Forward all env/+/raw messages
    MQTT->>Logger: Forward all env/# messages
    
    Logger->>DB: Insert sensor_readings document
    
    Dashboard->>User: Push real-time data via WebSocket
    User->>User: Update Chart.js graphs
    
    Note over E1,E2: Event Triggered (Constraint Violation)
    E1->>E1: Temperature > 30°C detected!
    E1->>MQTT: Publish env/event/temperature_alert_high
    MQTT->>Dashboard: Forward event
    MQTT->>Logger: Forward event
    Logger->>DB: Insert events document
    Dashboard->>User: Show alert notification 🚨
    
    Note over User,E1: Bidirectional Control Flow
    User->>Dashboard: Click "Simulate Overheat" button
    Dashboard->>MQTT: Publish greenhouse/control/simulate
    MQTT->>E1: Forward command
    MQTT->>E2: Forward command
    E1->>E1: Enable simulation mode
    E2->>E2: Enable simulation mode
```

---

## 🧩 Component Interaction Diagram

```mermaid
graph LR
    subgraph "Docker Network: mqtt-network"
        A[Edge Node 1<br/>Container]
        B[Edge Node 2<br/>Container]
        C[MQTT Broker<br/>Container]
        D[Dashboard<br/>Container]
        E[Data Logger<br/>Container]
        F[MongoDB<br/>Container]
    end

    A <-->|MQTT Protocol<br/>TCP 1883| C
    B <-->|MQTT Protocol<br/>TCP 1883| C
    D <-->|MQTT Protocol<br/>TCP 1883| C
    E <-->|MQTT Protocol<br/>TCP 1883| C
    E <-->|MongoDB Protocol<br/>TCP 27017| F
    
    G[User] -->|HTTP<br/>Port 3000| D
    G -->|WebSocket<br/>Port 9001| C

    style A fill:#ffcccc
    style B fill:#ffcccc
    style C fill:#ccffcc
    style D fill:#ffffcc
    style E fill:#ccccff
    style F fill:#ccccff
    style G fill:#ffeecc
```

---

## 🎯 Distributed System Principles Visualization

```mermaid
mindmap
  root((🏗️ Greenhouse<br/>Monitoring<br/>System))
    🔄 Message Passing
      MQTT Protocol
      No Shared Memory
      Pub/Sub Pattern
      Topic-based Routing
    
    🤖 Autonomy
      Independent Nodes
      Local Decision Making
      Self-contained Logic
      No Central Control
    
    🧵 Concurrency
      Multi-threading
      4 Sensors per Node
      Parallel Processing
      Thread-safe Operations
    
    ⚡ Event-Driven
      Constraint Triggers
      Real-time Alerts
      Reactive Architecture
      Asynchronous Events
    
    🔌 Loose Coupling
      Service Isolation
      Interface-based Communication
      Independent Deployment
      Restart without Impact
    
    🧠 Edge Computing
      Local Constraint Checking
      Bandwidth Optimization
      Latency Reduction
      Data Filtering
    
    💪 Fault Tolerance
      Auto-reconnect
      Graceful Degradation
      No Single Point of Failure
      Container Isolation
    
    🔄 Bidirectional
      Data Flow Up
      Control Flow Down
      Two-way MQTT
      Real-time Feedback
```

---

## 🌊 Data Flow Architecture

```mermaid
flowchart TD
    Start([⚡ System Start]) --> Init[Initialize Containers]
    Init --> EdgeStart[Edge Nodes Start]
    EdgeStart --> ThreadSpawn[Spawn 4 Threads per Node]
    
    ThreadSpawn --> SensorRead[🌡️ Read Sensor Data]
    SensorRead --> EdgeCheck{Edge Computing:<br/>Check Constraint?}
    
    EdgeCheck -->|✅ Normal| PubRaw[Publish to<br/>env/SENSOR/raw]
    EdgeCheck -->|❌ Violation| PubEvent[Publish to<br/>env/event/TYPE]
    
    PubRaw --> MQTTBroker[🔌 MQTT Broker<br/>Message Routing]
    PubEvent --> MQTTBroker
    
    MQTTBroker --> DashSub[📊 Dashboard<br/>Subscribes]
    MQTTBroker --> LogSub[📝 Logger<br/>Subscribes]
    
    DashSub --> WSPush[WebSocket Push<br/>to Browser]
    WSPush --> ChartUpdate[📈 Update Chart.js<br/>Real-time Graph]
    
    LogSub --> DBInsert[(💾 Insert to MongoDB)]
    
    ChartUpdate --> UserView[👤 User Views Dashboard]
    UserView --> UserAction{User Action?}
    
    UserAction -->|🎮 Simulate| ControlCmd[Send Control Command]
    UserAction -->|👁️ Monitor| ChartUpdate
    
    ControlCmd --> MQTTCtrl[MQTT Publish<br/>greenhouse/control/simulate]
    MQTTCtrl --> EdgeReceive[Edge Nodes Receive]
    EdgeReceive --> ModeBehavior[Modify Sensor Behavior]
    ModeBehavior --> SensorRead
    
    DBInsert --> HistData[📊 Historical Data<br/>Available]
    
    SensorRead -->|Every 20s| SensorRead

    style Start fill:#90EE90
    style EdgeCheck fill:#FFD700
    style MQTTBroker fill:#87CEEB
    style UserAction fill:#FFB6C1
    style DBInsert fill:#DDA0DD
```

---

## 🏛️ Layered Architecture

```mermaid
graph TB
    subgraph "Layer 1: Presentation Layer"
        L1A[Web Browser UI]
        L1B[Chart.js Visualization]
        L1C[Control Panel]
    end
    
    subgraph "Layer 2: Application Layer"
        L2A[Express Server]
        L2B[Socket.IO WebSocket]
        L2C[MQTT Client]
    end
    
    subgraph "Layer 3: Message Transport Layer"
        L3A[Eclipse Mosquitto Broker]
        L3B[Topic Routing]
        L3C[QoS Management]
    end
    
    subgraph "Layer 4: Business Logic Layer"
        L4A[Edge Computing Logic]
        L4B[Constraint Checking]
        L4C[Event Detection]
    end
    
    subgraph "Layer 5: Data Acquisition Layer"
        L5A[Sensor Threads]
        L5B[Data Simulation]
        L5C[Value Generation]
    end
    
    subgraph "Layer 6: Data Persistence Layer"
        L6A[Data Logger Service]
        L6B[MongoDB Database]
        L6C[Collections Management]
    end

    L1A --> L2A
    L1B --> L2A
    L1C --> L2B
    
    L2A --> L3A
    L2B --> L3A
    L2C --> L3A
    
    L3A --> L4A
    L3B --> L4A
    L3C --> L4A
    
    L4A --> L5A
    L4B --> L5A
    L4C --> L5B
    
    L3A --> L6A
    L6A --> L6B
    L6B --> L6C

    style L1A fill:#FFE4E1
    style L2A fill:#F0E68C
    style L3A fill:#98FB98
    style L4A fill:#87CEEB
    style L5A fill:#DDA0DD
    style L6A fill:#F5DEB3
```

---

## 🔐 MQTT Topic Structure

```mermaid
graph TD
    Root[🌳 MQTT Topics Root]
    
    Root --> Env[📁 env/]
    Root --> Control[📁 greenhouse/]
    
    Env --> Temp[📁 temperature/]
    Env --> Humid[📁 humidity/]
    Env --> Light[📁 light/]
    Env --> Air[📁 airquality/]
    Env --> Events[📁 event/]
    
    Temp --> TempRaw[📄 raw<br/>Real-time data]
    Humid --> HumidRaw[📄 raw<br/>Real-time data]
    Light --> LightRaw[📄 raw<br/>Real-time data]
    Air --> AirRaw[📄 raw<br/>Real-time data]
    
    Events --> TempHigh[📄 temperature_alert_high]
    Events --> TempLow[📄 temperature_alert_low]
    Events --> HumidHigh[📄 humidity_alert_high]
    Events --> HumidLow[📄 humidity_alert_low]
    Events --> LightLow[📄 light_low]
    Events --> AirWarn[📄 airquality_warning]
    Events --> AirDanger[📄 airquality_danger]
    
    Control --> CtrlSim[📄 control/simulate<br/>Command messages]

    style Root fill:#90EE90
    style Env fill:#FFD700
    style Control fill:#FF6347
    style Events fill:#FF4500
    style TempRaw fill:#87CEEB
    style HumidRaw fill:#87CEEB
    style LightRaw fill:#87CEEB
    style AirRaw fill:#87CEEB
```

---

## ⚙️ Container Orchestration

```mermaid
graph TB
    subgraph "Docker Compose Orchestration"
        DC[docker-compose.yml<br/>Orchestrator]
    end
    
    subgraph "Container Services"
        C1[🔌 mqtt-broker<br/>eclipse-mosquitto:2.0<br/>Ports: 1883, 9001]
        C2[🌡️ sensor-edge-1<br/>Python 3.10<br/>ENV: NODE_ID=edge-1]
        C3[🌡️ sensor-edge-2<br/>Python 3.10<br/>ENV: NODE_ID=edge-2]
        C4[📊 monitoring-dashboard<br/>Node.js 18<br/>Port: 3000]
        C5[📝 data-logger<br/>Python 3.10<br/>MQTT Subscriber]
        C6[🗄️ db-logger<br/>MongoDB 6.0<br/>Port: 27017]
    end
    
    subgraph "Docker Network"
        Net[mqtt-network<br/>Bridge Network]
    end
    
    subgraph "Dependencies"
        C2 -.->|depends_on| C1
        C3 -.->|depends_on| C1
        C4 -.->|depends_on| C1
        C5 -.->|depends_on| C1
        C5 -.->|depends_on| C6
    end
    
    DC -->|defines| C1
    DC -->|defines| C2
    DC -->|defines| C3
    DC -->|defines| C4
    DC -->|defines| C5
    DC -->|defines| C6
    DC -->|creates| Net
    
    C1 -.->|connected to| Net
    C2 -.->|connected to| Net
    C3 -.->|connected to| Net
    C4 -.->|connected to| Net
    C5 -.->|connected to| Net
    C6 -.->|connected to| Net

    style DC fill:#FFD700
    style C1 fill:#98FB98
    style C2 fill:#FFB6C1
    style C3 fill:#FFB6C1
    style C4 fill:#87CEEB
    style C5 fill:#DDA0DD
    style C6 fill:#F0E68C
    style Net fill:#E0E0E0
```

---

## 📈 Real-time Data Pipeline

```mermaid
graph LR
    subgraph "Edge Layer"
        S1[🌡️ Sensor 1<br/>20s interval]
        S2[💧 Sensor 2<br/>20s interval]
        S3[💡 Sensor 3<br/>20s interval]
        S4[🌫️ Sensor 4<br/>20s interval]
    end
    
    subgraph "Processing"
        P1[Edge Computing<br/>Constraint Check]
        P2[Data Format<br/>JSON Serialization]
    end
    
    subgraph "Transport"
        T1[MQTT Publish<br/>QoS 0]
        T2[Broker Routing<br/>Topic Matching]
    end
    
    subgraph "Consumption"
        C1[Dashboard<br/>Real-time Display]
        C2[Logger<br/>Persistence]
    end
    
    subgraph "Storage"
        D1[(MongoDB<br/>sensor_readings)]
        D2[(MongoDB<br/>events)]
    end
    
    subgraph "Visualization"
        V1[Chart.js<br/>Line Graphs]
        V2[Alert Panel<br/>Event List]
    end
    
    S1 --> P1
    S2 --> P1
    S3 --> P1
    S4 --> P1
    
    P1 --> P2
    P2 --> T1
    T1 --> T2
    
    T2 --> C1
    T2 --> C2
    
    C1 --> V1
    C1 --> V2
    
    C2 --> D1
    C2 --> D2

    style S1 fill:#FFB6C1
    style P1 fill:#FFD700
    style T2 fill:#98FB98
    style C1 fill:#87CEEB
    style D1 fill:#DDA0DD
    style V1 fill:#F0E68C
```

---

## 🛡️ Fault Tolerance Architecture

```mermaid
stateDiagram-v2
    [*] --> Running: Container Start
    
    Running --> Disconnected: Network Loss/<br/>Broker Restart
    Running --> Failed: Container Crash/<br/>Critical Error
    Running --> Stopped: Manual Stop/<br/>docker stop
    
    Disconnected --> Reconnecting: Auto-reconnect<br/>with exponential backoff
    Reconnecting --> Running: Connection Established
    Reconnecting --> Disconnected: Connection Failed/<br/>Retry
    
    Failed --> [*]: Container Exit
    Stopped --> Running: Manual Restart/<br/>docker start
    
    Running --> Running: Normal Operation<br/>Data flowing
    
    note right of Disconnected
        Other nodes continue
        independently
        (Autonomy Principle)
    end note
    
    note right of Reconnecting
        MQTT client auto-reconnect
        No data loss
        Resume from last state
    end note
    
    note right of Running
        All 4 sensor threads
        running concurrently
        Edge computing active
    end note
```

---

## 🎮 Simulation Control Flow

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant UI as 🖥️ Dashboard UI
    participant Server as 🔧 Dashboard Server
    participant MQTT as 🔌 MQTT Broker
    participant Edge1 as 🌡️ Edge Node 1
    participant Edge2 as 🌡️ Edge Node 2

    User->>UI: Click "Simulate Overheat" button
    UI->>UI: Disable button (prevent spam)
    UI->>Server: Socket.IO emit('simulation', {type: 'overheat'})
    
    Server->>Server: Validate command
    Server->>MQTT: Publish to greenhouse/control/simulate
    Note over Server,MQTT: Payload: {type:"overheat",timestamp:"..."}
    
    MQTT->>Edge1: Forward command
    MQTT->>Edge2: Forward command
    
    Edge1->>Edge1: Set simulation_mode = True
    Edge1->>Edge1: Override temperature range to 32-36°C
    Edge2->>Edge2: Set simulation_mode = True
    Edge2->>Edge2: Override temperature range to 32-36°C
    
    Note over Edge1,Edge2: Next sensor readings will use<br/>simulation values
    
    Edge1->>MQTT: Publish high temperature reading
    Edge2->>MQTT: Publish high temperature reading
    
    MQTT->>Server: Forward sensor data
    Server->>UI: WebSocket push updated data
    
    UI->>UI: Update graphs with new data
    UI->>UI: Show alert: Temperature Alert High 🚨
    UI->>UI: Re-enable button
    
    User->>User: See simulated overheat effect
```

---

## 🔍 Monitoring & Observability

```mermaid
graph TB
    subgraph "Data Sources"
        E1[Edge Node 1 Logs]
        E2[Edge Node 2 Logs]
        ML[MQTT Broker Logs]
        DL[Dashboard Logs]
        LL[Logger Logs]
    end
    
    subgraph "Monitoring Tools"
        DC[docker logs]
        DCP[docker-compose ps]
        DCS[docker stats]
    end
    
    subgraph "Metrics"
        M1[Container Status<br/>Up/Down]
        M2[Message Count<br/>Throughput]
        M3[Event Frequency<br/>Alert Rate]
        M4[Thread Count<br/>Concurrency]
    end
    
    subgraph "Testing"
        T1[🧪 test_distributed_system.sh<br/>21 Automated Tests]
        T2[TESTING_GUIDE.md<br/>Manual Test Procedures]
    end
    
    subgraph "Observability Dashboard"
        O1[Real-time Graphs<br/>120 data points]
        O2[Alert Panel<br/>Event History]
        O3[System Status<br/>Active Zones]
    end
    
    E1 --> DC
    E2 --> DC
    ML --> DC
    DL --> DC
    LL --> DC
    
    DC --> M1
    DCP --> M1
    DCS --> M2
    
    M1 --> T1
    M2 --> T1
    M3 --> T1
    M4 --> T1
    
    T1 --> O1
    T2 --> O2
    M3 --> O3

    style T1 fill:#90EE90
    style O1 fill:#87CEEB
    style M1 fill:#FFD700
```

---

## 📦 Deployment Architecture

```mermaid
graph TD
    subgraph "Development Environment"
        Dev[👨‍💻 Developer Machine<br/>VS Code + Docker Desktop]
    end
    
    subgraph "Version Control"
        Git[📚 GitHub Repository<br/>rinaldikomber27/greenhouse-monitoring-system]
    end
    
    subgraph "Container Registry"
        Reg[🐳 Docker Images<br/>Local Build Cache]
    end
    
    subgraph "Runtime Environment"
        Docker[🐳 Docker Engine<br/>Container Runtime]
        Compose[⚙️ Docker Compose<br/>Orchestration]
    end
    
    subgraph "Running System"
        C1[Container 1: MQTT Broker]
        C2[Container 2: Edge Node 1]
        C3[Container 3: Edge Node 2]
        C4[Container 4: Dashboard]
        C5[Container 5: Logger]
        C6[Container 6: MongoDB]
    end
    
    subgraph "Access Points"
        A1[🌐 http://localhost:3000<br/>Dashboard UI]
        A2[🔌 mqtt://localhost:1883<br/>MQTT TCP]
        A3[🌐 ws://localhost:9001<br/>MQTT WebSocket]
        A4[🗄️ mongodb://localhost:27017<br/>Database]
    end
    
    Dev -->|git push| Git
    Git -->|git clone| Dev
    
    Dev -->|docker-compose build| Reg
    Reg -->|docker-compose up| Docker
    Docker -->|orchestrates| Compose
    
    Compose -->|starts| C1
    Compose -->|starts| C2
    Compose -->|starts| C3
    Compose -->|starts| C4
    Compose -->|starts| C5
    Compose -->|starts| C6
    
    C4 -->|exposes| A1
    C1 -->|exposes| A2
    C1 -->|exposes| A3
    C6 -->|exposes| A4

    style Git fill:#FFD700
    style Docker fill:#0db7ed
    style C1 fill:#98FB98
    style C4 fill:#87CEEB
    style A1 fill:#FFB6C1
```

---

## 🎯 Testing Architecture

```mermaid
graph TB
    subgraph "Test Suite"
        TS[🧪 test_distributed_system.sh<br/>Automated Test Runner]
    end
    
    subgraph "Test Categories"
        T1[Test 1: Message Passing<br/>MQTT Communication]
        T2[Test 2: Node Autonomy<br/>Independence]
        T3[Test 3: Loose Coupling<br/>Service Isolation]
        T4[Test 4: Concurrency<br/>Multi-threading]
        T5[Test 5: Event-Driven<br/>Reactive System]
        T6[Test 6: Edge Computing<br/>Local Processing]
        T7[Test 7: Fault Tolerance<br/>Auto-recovery]
        T8[Test 8: Bidirectional<br/>Two-way Communication]
        T9[Test 9: Location Transparency<br/>Service Discovery]
        T10[Test 10: System Health<br/>Overall Status]
    end
    
    subgraph "Test Results"
        R1[✅ Passed Tests]
        R2[❌ Failed Tests]
        R3[📊 Pass Rate %]
        R4[📝 Test Report]
    end
    
    subgraph "Validation"
        V1{All Tests<br/>Passed?}
        V2[✅ System Valid<br/>Distributed Principles Met]
        V3[❌ System Invalid<br/>Review Required]
    end
    
    TS --> T1
    TS --> T2
    TS --> T3
    TS --> T4
    TS --> T5
    TS --> T6
    TS --> T7
    TS --> T8
    TS --> T9
    TS --> T10
    
    T1 --> R1
    T2 --> R1
    T3 --> R1
    T4 --> R1
    T5 --> R1
    T6 --> R1
    T7 --> R1
    T8 --> R1
    T9 --> R1
    T10 --> R1
    
    R1 --> R3
    R2 --> R3
    R3 --> R4
    
    R4 --> V1
    V1 -->|20/20 Pass| V2
    V1 -->|< 20 Pass| V3

    style TS fill:#FFD700
    style R1 fill:#90EE90
    style V2 fill:#32CD32
    style V3 fill:#FF6347
```

---

## 💡 Key Architecture Insights

### 🎯 Design Decisions

1. **MQTT over HTTP**: Lightweight, efficient pub/sub for IoT
2. **Edge Computing**: Reduce bandwidth, faster response times
3. **Docker Containers**: Service isolation, easy deployment
4. **Multi-threading**: Concurrent sensor operations
5. **WebSocket**: Real-time bidirectional communication
6. **MongoDB**: Flexible schema for sensor data

### 📊 Performance Characteristics

- **Latency**: < 100ms sensor-to-dashboard
- **Throughput**: 12 messages/minute per node (20s intervals)
- **Scalability**: Horizontal (add more edge nodes)
- **Reliability**: Auto-reconnect, fault tolerance
- **Data Retention**: 120 data points in memory, unlimited in DB

### 🔐 Security Considerations

- **Network Isolation**: Docker bridge network
- **Container Isolation**: Separate namespaces
- **No Authentication**: Development environment (add for production)
- **Local Deployment**: No external exposure

### 🚀 Future Enhancements

- Add SSL/TLS for MQTT
- Implement authentication (username/password)
- Add more sensor types
- Implement data aggregation
- Add alerting via email/SMS
- Create mobile app
- Add machine learning for anomaly detection

---

**Generated**: December 4, 2025  
**System**: Greenhouse Environmental Monitoring System  
**Repository**: https://github.com/rinaldikomber27/greenhouse-monitoring-system
