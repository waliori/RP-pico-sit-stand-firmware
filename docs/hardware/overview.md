# Hardware Overview

Hardware components and connections for the Smart Sit-Stand Desk Controller.

## 🔌 Core Components

### Primary Controller
- **Raspberry Pi Pico W** - Main microcontroller with WiFi

### Motor Control System
- **BTS7960B H-Bridge** - Motor driver module
- **37GB555 Geared Motor** - 12V 180RPM DC motor with encoder

### Sensor System
- **ACS712-30A** - Current sensor module
- **ADXL345** - 3-axis accelerometer

### User Interface
- **SH1106 OLED** - 128x64 monochrome display
- **KY-040 Rotary Encoder** - 360° rotary encoder with button (1x UI navigation)
- **KY-040 Rotary Encoder** - 360° rotary encoder (1x motor position feedback)
- **Tactile Buttons** - Push buttons for controls (5x)

### Additional Components
- **12V Power Adapter** - AC to DC power supply
- **LM2596 Buck Converter** - DC-DC step down module
- **Buzzer** - Piezo buzzer (PWM driven)
- **Vibration Motor** - Coin vibration motor 3V
- **Connection Wires** - For linking components
- **3D Printed Enclosures** - Custom housings and mounts (CAD files available)

## 🔗 Pin Assignments

| GPIO | Function | Component | Notes |
|------|----------|-----------|-------|
| 0 | PWM | H-Bridge R_PWM | Motor forward |
| 1 | PWM | H-Bridge L_PWM | Motor reverse |
| 4 | I2C SDA | OLED Display | I2C0 Bus |
| 5 | I2C SCL | OLED Display | I2C0 Bus |
| 6 | I2C SDA | Accelerometer | I2C1 Bus |
| 7 | I2C SCL | Accelerometer | I2C1 Bus |
| 9 | Digital | Preset Button 1 | Internal pull-up |
| 10 | Digital | Preset Button 2 | Internal pull-up |
| 11 | Digital | Preset Button 3 | Internal pull-up |
| 13 | Digital | UI Encoder SW | Button switch (right encoder) |
| 14 | Digital | UI Encoder DT | Data signal (right encoder) |
| 15 | Digital | UI Encoder CLK | Clock signal (right encoder) |
| 16 | Digital | Vibration Motor | Output |
| 20 | Digital | Position Enc CLK | Motor encoder (left encoder) |
| 21 | Digital | Position Enc DT | Motor encoder (left encoder) |
| 22 | PWM | Buzzer | Audio feedback |
| 26 | Digital | Down Button | Motor control |
| 27 | Digital | Up Button | Motor control |
| 28 | ADC | Current Sensor | Analog input |

## ⚡ Power Configuration

```
Power Rails:
├── 12V (Motor Power)
│   └── Linear Actuator (via H-Bridge)
│
├── 3.3V (All Electronics)
│   ├── Raspberry Pi Pico W
│   ├── H-Bridge Control Logic
│   ├── OLED Display (SH1106)
│   ├── Accelerometer (ADXL345)
│   ├── Current Sensor (ACS712)
│   ├── Rotary Encoders
│   ├── Tactile Buttons
│   ├── Buzzer
│   └── Vibration Motor
│
└── GND (Common Ground)
    └── All components share common ground
```

## 🔌 Connection Summary

### I2C Bus Configuration
```
I2C0 (Display):          I2C1 (Sensors):
GPIO 4 (SDA) ──── OLED   GPIO 6 (SDA) ──── ADXL345
GPIO 5 (SCL) ──── OLED   GPIO 7 (SCL) ──── ADXL345
```

### Motor Control
```
GPIO 0 → H-Bridge R_PWM (Forward)
GPIO 1 → H-Bridge L_PWM (Reverse)
GPIO 20 → Position Encoder CLK
GPIO 21 → Position Encoder DT
GPIO 28 → Current Sensor Output
```

### User Interface
```
GPIO 13 → UI Encoder Button (right encoder)
GPIO 14 → UI Encoder DT (right encoder)
GPIO 15 → UI Encoder CLK (right encoder)
GPIO 26 → Down Button
GPIO 27 → Up Button
GPIO 9/10/11 → Preset Buttons 1/2/3
```

**Note**: All buttons use the Pico W's internal pull-up resistors - no external resistors needed.

**Encoder Configuration**:
- **Left Encoder**: Position feedback only (GPIO 20/21)
- **Right Encoder**: UI navigation with button (GPIO 13/14/15)