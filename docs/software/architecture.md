# Software Architecture

This document provides a comprehensive overview of the software architecture for the Smart Sit-Stand Desk Controller, including system design patterns, module organization, and data flow.

## 🏗️ Architectural Overview

The software follows a **layered architecture** pattern with clear separation of concerns, implementing **object-oriented design** principles for maintainability and extensibility.

```
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  main.py           │  Application bootstrap and main loop   │
│  menu.py           │  User interface state management       │
│  wifi.py           │  Network services and web interface    │
├─────────────────────────────────────────────────────────────┤
│                     BUSINESS LOGIC LAYER                    │
├─────────────────────────────────────────────────────────────┤
│  motor.py          │  Motor control and basic safety        │
│  calibration.py    │  System configuration and calibration  │
│  presets.py        │  Height preset management              │
│  collision.py      │  🚧 Collision detection (WIP)          │
├─────────────────────────────────────────────────────────────┤
│                     HARDWARE ABSTRACTION LAYER              │
├─────────────────────────────────────────────────────────────┤
│  display.py        │  OLED display management               │
│  accelerometer.py  │  Motion sensor interface               │
│  acs712.py         │  Current sensor interface              │
│  buzz_vib.py       │  Audio/haptic feedback                 │
├─────────────────────────────────────────────────────────────┤
│                     DRIVER LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  sh1106.py         │  OLED display driver                   │
│  writer.py         │  Font rendering system                 │
│  songs.py          │  Audio pattern definitions             │
│  rtttl.py          │  Music format parser                   │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Design Principles

### 1. Separation of Concerns
- **Hardware abstraction** isolates low-level sensor/actuator interfaces
- **Business logic** implements core functionality independent of hardware
- **User interface** handles presentation and user interaction
- **Network services** manage connectivity and remote access

### 2. Thread Safety
- **Shared resources** protected with locks (`_thread.allocate_lock()`)
- **Critical sections** properly synchronized for display and file I/O
- **Atomic operations** for sensor readings and motor control

### 3. Fault Tolerance
- **Graceful degradation** when components fail
- **Error recovery** mechanisms for network and hardware issues
- **Safe defaults** for all configuration parameters
- **Watchdog timers** for critical operations

### 4. Modularity
- **Loose coupling** between modules through well-defined interfaces
- **High cohesion** within individual modules
- **Dependency injection** for testability and flexibility
- **Plugin architecture** for future extensions

## 📊 Data Flow Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Sensors   │───►│   Motor     │───►│ Collision   │
│             │    │  Control    │    │ Detection   │
│ • ADXL345   │    │             │    │             │
│ • ACS712    │    │ • Position  │    │ • PCA       │
│ • Encoder   │    │ • Speed     │    │ • Threshold │
└─────────────┘    │ • Current   │    │ • Safety    │
                   └─────────────┘    └─────────────┘
                          │                   │
                          ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Display   │    │   Safety    │
                   │   System    │    │  Actions    │
                   │             │    │             │
                   │ • Status    │    │ • Stop      │
                   │ • Height    │    │ • Alert     │
                   │ • Menu      │    │ • Log       │
                   └─────────────┘    └─────────────┘
                          ▲
                          │
                   ┌─────────────┐    ┌─────────────┐
                   │ User Input  │    │    WiFi     │
                   │             │    │   API       │
                   │ • Buttons   │───►│             │
                   │ • Encoder   │    │ • REST      │
                   │ • Menu      │    │ • WebSocket │
                   └─────────────┘    └─────────────┘
```

## 🔧 Module Architecture

### Core Control Module (`motor.py`)

**Class: Motor**
```python
class Motor:
    def __init__(self, pwm1, pwm2, counter, sLock, accelO, curr_sens):
        # Hardware interfaces
        self.pwm1 = pwm1              # Forward PWM (GPIO 0)
        self.pwm2 = pwm2              # Reverse PWM (GPIO 1)
        self.counter = counter        # Position encoder (left encoder, GPIO 20/21)
        self.sLock = sLock           # Thread lock
        self.accelO = accelO         # Accelerometer object (GPIO 6/7)
        self.curr_sens = curr_sens   # Current sensor object (GPIO 28)
        
        # State variables
        self.direction = 0           # 0=stop, 1=up, -1=down
        self.rpm = 0                 # Current RPM
        self.blocked = False         # Collision state
        
        # PCA variables for collision detection
        self.principal_components_up = None
        self.principal_components_down = None
        self.projected_mean_up = None
        self.projected_mean_down = None
```

**Key Methods:**
- `move_motor()` - Manual button control with safety
- `move_motor_height()` - Automated movement to specific position
- `move_motor_api()` - Asynchronous API-controlled movement
- `encoder()` - Position tracking and RPM calculation
- `rpm_updt()` - Sensor data collection and processing
- **Future**: `update_pca()` - Real-time PCA learning and analysis ⚠️ *Under Development*

### Collision Detection Module (`collision.py`) 🚧 *Work In Progress*

**⚠️ Development Status**: This module is currently under active development as part of the [Micropython sit/stand smart table project](https://github.com/users/waliori/projects/1).

**Current Implementation**:
```python
class Collision:
    def __init__(self, calibrationO):
        # Basic framework in place
        self.calibration_data = calibrationO.calib
        # Advanced algorithm implementation in progress
```

**Planned Algorithm Overview (Under Development)**:
1. **Data Collection**: Multi-sensor readings (accelerometer, current, RPM)
2. **Normalization**: Scale all sensor values to 0-1 range  
3. **PCA Projection**: Project onto learned principal components
4. **Distance Calculation**: Mahalanobis distance from normal operation
5. **Adaptive Thresholding**: Dynamic threshold based on historical data
6. **Decision Making**: Collision detected if distance exceeds threshold

**Implementation Status**: Basic class structure exists, advanced PCA algorithm in development.

### Display Management (`display.py`)

**Class: Display**
```python
class Display:
    def __init__(self, width, height, i2c_id, scl, sda, buzzvibO, freq=400000):
        self.oled = SH1106_I2C(width, height, i2c, rotate=180)  # I2C0, GPIO 4/5
        self.font_writer_20 = writer.Writer(self.oled, freesans20)
        self.font_writer_30 = writer.Writer(self.oled, firacodeBold30)
        
        # UI encoder interface (right encoder, GPIO 13/14/15)
        self.ui_encoder_clk = Pin(15, Pin.IN, Pin.PULL_UP)
        self.ui_encoder_dt = Pin(14, Pin.IN, Pin.PULL_UP)
        self.ui_encoder_sw = Pin(13, Pin.IN, Pin.PULL_UP)
        
        # Menu state
        self.menu_line = 1
        self.menu_highlight = 1
        self.menu_shift = 0
        
        # Power management
        self.sleep_state = False
        self.reminder_time = 0
```

**Key Features:**
- **Multi-font rendering** with custom font files
- **Icon system** for status indicators (WiFi, lock, sound)
- **Menu framework** with scrolling and highlighting (right encoder navigation)
- **Power management** with sleep/wake functionality
- **Animation support** for progress bars and transitions
- **Dual encoder support**: Position feedback (left) and UI navigation (right)

### Network Services (`wifi.py`)

**Class: Wifi**
```python
class Wifi:
    def __init__(self, app, sLock, displayO, menuO):
        self.wlan = network.WLAN(network.STA_IF)  # Station mode
        self.ap = network.WLAN(network.AP_IF)     # Access Point mode
        self.app = app                            # Microdot web framework
        self.saved_json = {}                      # Saved networks
```

**Network Modes:**
1. **Station Mode**: Connect to existing WiFi networks
2. **Access Point Mode**: Create configuration hotspot
3. **Dual Mode**: Station + AP for setup and operation

**Web Interface Features:**
- **Configuration Portal**: WiFi setup and network management
- **REST API**: Complete motor control and status endpoints
- **Real-time Updates**: WebSocket for live status monitoring
- **Security**: Saved network credentials and access control

## 🔄 Concurrency Model

### Thread Architecture

```
Main Thread (Core 0):
├── Hardware Initialization
├── Sensor Reading Loop
├── Motor Control Logic
├── Collision Detection
└── Display Updates

Network Thread (Core 1):
├── WiFi Management
├── Web Server (Microdot)
├── API Request Handling
└── WebSocket Communications

Shared Resources:
├── Display (sLock protected)
├── Motor State (atomic operations)
├── Configuration Files (sLock protected)
└── Sensor Data (lock-free queues)
```

### Synchronization Mechanisms

**Thread Locks (`_thread.allocate_lock()`)**:
```python
sLock = _thread.allocate_lock()

# Protected operations
sLock.acquire()
try:
    # Critical section
    display.update()
    file.write(data)
finally:
    sLock.release()
```

**Async/Await Pattern**:
```python
async def move_motor_api(self, direction, outA, outB, mini, maxi):
    while self.api:
        # Non-blocking motor control
        await asyncio.sleep_ms(1)
```

## 💾 Data Management

### Configuration Storage

**JSON-based Configuration**:
```python
# settings.json - System configuration
{
    "min_encoder": 0,
    "max_encoder": 5000,
    "min_real": 72.0,
    "max_real": 120.0,
    "sleep_time": 30,
    "reminder_time": 5400,
    "principal_components_up": [[...], [...]],
    "principal_components_down": [[...], [...]]
}

# presets.json - Height presets
{
    "1": 2500,
    "2": 3750, 
    "3": 4200
}

# saved_wifi.json - Network credentials
{
    "HomeNetwork": "password123",
    "OfficeWiFi": "securepass456"
}

# state.json - Current position
{
    "current_encoder": 2800
}
```

### File I/O Patterns

**Thread-safe File Operations**:
```python
def save_settings(self, data):
    self.sLock.acquire()
    try:
        with open("settings.json", "w") as file:
            file.write(json.dumps(data))
    finally:
        self.sLock.release()
```

**Error Handling**:
```python
try:
    with open("settings.json", "r") as file:
        settings = json.load(file)
except (OSError, ValueError):
    # Create default configuration
    settings = self.create_default_settings()
    self.save_settings(settings)
```

## 🔐 Security Architecture

### Access Control

**Physical Security**:
- Lock/unlock state prevents movement
- Emergency stop capability
- Position limits enforced

**Network Security**:
- WPA3 WiFi encryption
- CORS headers for web API
- Input validation and sanitization
- Rate limiting (future enhancement)

### Error Handling Strategy

**Graceful Degradation**:
```python
def safe_operation(self, operation):
    try:
        return operation()
    except HardwareError as e:
        self.log_error(e)
        self.enter_safe_mode()
        return default_value
    except NetworkError as e:
        self.log_error(e)
        self.continue_offline()
        return cached_value
```

**Recovery Mechanisms**:
- Hardware watchdog timers
- Software watchdog for critical loops
- Automatic retry for transient failures
- Factory reset capability

## 📊 Performance Characteristics

### Real-time Requirements

| Operation | Max Latency | Frequency | Priority |
|-----------|-------------|-----------|----------|
| Collision Detection | 10ms | 100Hz | Critical |
| Position Feedback | 20ms | 50Hz | High |
| Display Update | 50ms | 20Hz | Medium |
| Network Response | 200ms | Variable | Low |

### Memory Usage

**Static Memory**:
- Code: ~150KB
- Fonts: ~20KB  
- Constants: ~5KB

**Dynamic Memory**:
- Sensor buffers: ~2KB
- Network buffers: ~8KB
- Display buffers: ~1KB
- Stack space: ~4KB per thread

### Resource Optimization

**CPU Usage**:
- Core 0: 60% (control loops)
- Core 1: 40% (network services)

**Power Optimization**:
- Sleep mode for display
- WiFi power management
- Sensor duty cycling

## 🧪 Testing Architecture

### Unit Testing Framework

**Hardware Mocking**:
```python
class MockSensor:
    def __init__(self, test_data):
        self.test_data = test_data
        self.index = 0
    
    def read(self):
        data = self.test_data[self.index]
        self.index = (self.index + 1) % len(self.test_data)
        return data
```

**Test Categories**:
1. **Unit Tests**: Individual module functionality
2. **Integration Tests**: Module interactions
3. **Hardware Tests**: Real hardware verification
4. **Stress Tests**: Continuous operation and edge cases

### Debugging Infrastructure

**Logging System**:
```python
DEBUG = True

def log_debug(message, category="GENERAL"):
    if DEBUG:
        timestamp = utime.ticks_ms()
        print(f"[{timestamp}] {category}: {message}")
```

**Performance Monitoring**:
- Execution time measurement
- Memory usage tracking
- Network latency monitoring
- Sensor data validation

## 🔄 Maintenance and Updates

### Code Organization

**File Structure**:
```
/
├── main.py              # Application entry point
├── motor.py             # Core motor control
├── collision.py         # Collision detection
├── calibration.py       # System calibration
├── wifi.py              # Network services
├── display.py           # Display management
├── menu.py              # User interface
├── presets.py           # Height presets
├── accelerometer.py     # Sensor interface
├── acs712.py            # Current sensor
├── buzz_vib.py          # Feedback systems
├── sh1106.py            # Display driver
├── writer.py            # Font rendering
├── songs.py             # Audio patterns
├── rtttl.py             # Music parser
├── freesans20.py        # Font data
└── firacodeBold30.py    # Font data
```

**Coding Standards**:
- PEP 8 Python style guide
- Comprehensive docstrings
- Type hints where applicable
- Error handling for all I/O operations

### Version Management

**Configuration Version Tracking**:
```python
CONFIG_VERSION = "1.0"

def migrate_config(old_config, old_version):
    if old_version < "1.0":
        # Migration logic
        pass
    return updated_config
```

**Over-the-Air Updates** (Future):
- Secure firmware updates via WiFi
- Configuration backup and restore
- Rollback capability for failed updates

---

**Next Steps**: Review [Module Reference](modules.md) for detailed API documentation and [Collision Detection](collision-detection.md) for algorithm implementation details.