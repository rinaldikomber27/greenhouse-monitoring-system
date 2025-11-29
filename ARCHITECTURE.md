# Distributed System Architecture - Technical Documentation

## System Overview

This project implements a **distributed environmental monitoring system** using modern distributed computing principles. The system is designed to demonstrate key concepts in distributed systems, edge computing, and event-driven architecture.

## Architecture Principles

### 1. Message Passing vs Shared Memory

**Traditional Approach (Shared Memory)**:
```
┌─────────┐     ┌─────────┐
│Process A│ ──→ │ Shared  │ ←── │Process B│
└─────────┘     │ Memory  │     └─────────┘
                └─────────┘
❌ Race conditions
❌ Synchronization overhead
❌ Tight coupling
```

**Our Approach (Message Passing)**:
```
┌─────────┐                    ┌─────────┐
│Process A│ ──→ [MQTT] ──→     │Process B│
└─────────┘                    └─────────┘
✅ No shared state
✅ Loose coupling
✅ Location transparency
```

### 2. Edge Computing

**Edge computing** moves computation closer to data sources, reducing:
- Latency
- Bandwidth usage
- Central processing load

**Implementation in this system**:
```python
# Edge Node performs local computation
def check_constraint(sensor_type, value):
    if sensor_type == 'temperature':
        if value > 30:  # Local decision
            return True, 'temperature_alert'
    return False, None
```

Only meaningful data (normal + alerts) is transmitted to central systems.

### 3. Event-Driven Architecture

**Traditional Polling**:
```
while True:
    check_sensor()
    if abnormal: alert()
    sleep(interval)
```
❌ Wastes resources checking unchanged data

**Event-Driven (Our Implementation)**:
```
on_sensor_read(value):
    if violates_constraint(value):
        publish_event('alert')  # ✅ React only when needed
```

### 4. Concurrency Model

Each sensor runs in its own thread:

```python
threads = [
    Thread(target=sensor_thread, args=('temperature',)),
    Thread(target=sensor_thread, args=('humidity',)),
    Thread(target=sensor_thread, args=('light',)),
    Thread(target=sensor_thread, args=('airquality',))
]
```

Benefits:
- ✅ True parallelism
- ✅ Independent sensor intervals
- ✅ Non-blocking operations
- ✅ Better resource utilization

## Distributed System Characteristics

### 1. Transparency
- **Location Transparency**: Services don't need to know physical location of others
- **Access Transparency**: All services accessed via MQTT protocol
- **Failure Transparency**: Service failures don't cascade

### 2. Scalability
```yaml
# Add new edge node easily
sensor-edge-3:
  build: ./edge
  environment:
    - NODE_ID=edge-3
```
No code changes needed in other services.

### 3. Fault Tolerance
```bash
# If edge-1 fails, edge-2 continues
docker stop edge-node-1  # edge-2 unaffected

# Restart without data loss
docker start edge-node-1  # Reconnects automatically
```

### 4. Heterogeneity
- Edge nodes: Python
- Dashboard: Node.js
- Broker: C/C++ (Mosquitto)
- Database: MongoDB

Different technologies work together via standard protocol (MQTT).

## Communication Patterns

### Publish-Subscribe Pattern

```
Publisher (Edge Node)          Subscriber (Dashboard)
     │                              │
     ├──→ publish(topic, data)      │
     │         ↓                     │
     │    [MQTT Broker]              │
     │         ↓                     │
     │    ←───────subscribe(topic)──┤
     │                              │
     └──→ notify(data) ──→──→──→──→┘
```

Benefits:
- Decoupling of producers and consumers
- Many-to-many communication
- Dynamic subscription

### Quality of Service (QoS)

MQTT supports 3 QoS levels:
- QoS 0: At most once (fire and forget)
- QoS 1: At least once (acknowledged delivery)
- QoS 2: Exactly once (assured delivery)

Our system uses QoS 0 for real-time data (acceptable loss) but could upgrade to QoS 1 for critical events.

## Data Flow Analysis

### Normal Data Flow
```
[Sensor Thread] → [Constraint Check] → [MQTT Publish]
     ↓                    ↓                  ↓
   5-10s              Local            env/*/raw
                    Decision
```

**Latency**: ~10-50ms (sensor → broker → subscriber)

### Event Flow
```
[Sensor Thread] → [Constraint Violated!] → [MQTT Publish]
     ↓                    ↓                      ↓
  Real-time          Event=True           env/event/*
                                              ↓
                                          [Dashboard Alert]
                                              ↓
                                          [User Notified]
```

**Latency**: ~50-100ms (end-to-end event notification)

## Performance Considerations

### Thread Safety
```python
# Thread-safe MQTT operations
self.client.publish(topic, payload)  # Paho-MQTT handles locking
```

### Memory Management
```javascript
// Dashboard maintains sliding window
const maxDataPoints = 50;
if (dataset.data.length > maxDataPoints) {
    dataset.data.shift();  // Remove oldest
}
```

### Network Optimization
- Lightweight JSON payloads (~100 bytes)
- Persistent MQTT connections
- WebSocket for dashboard (push vs pull)

## Security Considerations

**Current Implementation** (Development):
- Anonymous MQTT access
- No encryption

**Production Recommendations**:
```conf
# mosquitto.conf
allow_anonymous false
password_file /mosquitto/config/passwd

listener 8883
certfile /mosquitto/config/server.crt
keyfile /mosquitto/config/server.key
```

## Testing Strategies

### Unit Testing
```python
# Test constraint logic
def test_temperature_constraint():
    assert check_constraint('temperature', 35) == (True, 'alert')
    assert check_constraint('temperature', 25) == (False, None)
```

### Integration Testing
```bash
# Test MQTT communication
mosquitto_pub -t 'env/test' -m '{"test": true}'
mosquitto_sub -t 'env/#' -C 1  # Receive one message
```

### Load Testing
```bash
# Simulate multiple edge nodes
for i in {1..10}; do
    docker-compose up -d --scale sensor-edge=$i
done
```

## Monitoring & Observability

### Log Aggregation
```bash
# Centralized logging
docker-compose logs -f | grep "ERROR\|WARN"
```

### Metrics to Track
- Message throughput (messages/sec)
- Edge-to-dashboard latency
- Event frequency
- Resource utilization (CPU, memory)

### Health Checks
```yaml
healthcheck:
  test: ["CMD", "mosquitto_sub", "-t", "$$SYS/#", "-C", "1"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Future Enhancements

1. **Service Discovery**: Consul/Etcd for dynamic service registry
2. **Load Balancing**: HAProxy for MQTT broker cluster
3. **Message Persistence**: Retain messages for offline subscribers
4. **API Gateway**: REST API for external integration
5. **Machine Learning**: Anomaly detection on edge nodes
6. **Security**: TLS/SSL encryption, authentication, authorization

## References

- Tanenbaum, A. S., & Van Steen, M. (2017). *Distributed Systems: Principles and Paradigms*
- Coulouris, G., et al. (2011). *Distributed Systems: Concepts and Design*
- MQTT Specification: https://mqtt.org/mqtt-specification/
- Edge Computing Whitepaper: https://www.etsi.org/technologies/edge-computing

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-29
