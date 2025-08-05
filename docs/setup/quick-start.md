# Quick Start Guide

Get your Smart Sit-Stand Desk Controller running with this setup guide.

🎬 **[Watch the Build Journey](https://www.youtube.com/watch?v=PKzvHBzcGJ4)** - Experience the development adventure and see how to use the finished system.

## ⚡ Prerequisites

- ✅ **Raspberry Pi Pico W** with MicroPython firmware installed
- ✅ **All hardware components** from the [Bill of Materials](../hardware/bom.md)
- ✅ **USB cable** for programming and power
- ✅ **Computer** with Thonny IDE installed

📺 **Pro Tip**: Watch the [build video](https://www.youtube.com/watch?v=PKzvHBzcGJ4) to experience the development journey and see the finished system in action.

## 🔧 Hardware Assembly

Connect components according to the pin configuration in [Hardware Overview](../hardware/overview.md):

**Power Connections:**
```
Pico W 3V3 → All electronics (OLED, ADXL345, ACS712, Encoders, Buttons)
Pico W GND → All component grounds
12V Supply → Motor via H-Bridge only
```

**I2C Connections:**
```
GPIO 4 → OLED SDA        GPIO 6 → ADXL345 SDA  
GPIO 5 → OLED SCL        GPIO 7 → ADXL345 SCL
```

**Motor Control:**
```
GPIO 0 → H-Bridge R_PWM
GPIO 1 → H-Bridge L_PWM
GPIO 20 → Position Encoder CLK
GPIO 21 → Position Encoder DT
GPIO 28 → Current Sensor Output
```

**User Interface:**
```
GPIO 13 → UI Encoder Button (right encoder)
GPIO 14 → UI Encoder DT (right encoder)
GPIO 15 → UI Encoder CLK (right encoder)
GPIO 26 → Down Button
GPIO 27 → Up Button
GPIO 9/10/11 → Preset Buttons 1/2/3
```

**Note**: The system uses two separate rotary encoders:
- **Left Encoder** (GPIO 20/21): Motor position feedback only
- **Right Encoder** (GPIO 13/14/15): UI navigation with button

## 💻 Software Installation

### Download and Install

```bash
# Clone the repository
git clone https://github.com/waliori/RP-pico-sit-stand-firmware.git
cd RP-pico-sit-stand-firmware
```

### Upload to Pico W using Thonny

1. Open **Thonny IDE**
2. Configure interpreter: **"MicroPython (Raspberry Pi Pico)"**
3. Upload all `.py` files to the Pico W
4. Run `main.py`

## ⚙️ Initial Configuration

### Height Calibration

When you first power on, the system enters calibration mode:

1. **Move to Highest Position** using manual controls
   - Press and hold the rotary encoder button
   - "Max encoder set" appears on display

2. **Set Real Height Value**
   - Turn rotary encoder to set actual height (e.g., 120.0 cm)
   - Press encoder button to confirm

3. **Move to Lowest Position** using manual controls
   - Press and hold the rotary encoder button
   - "Min encoder set" appears

4. **Set Minimum Height Value**
   - Turn encoder to set actual height (e.g., 72.0 cm)
   - Press encoder button to confirm
   - System saves settings and exits calibration

### WiFi Setup

1. **Access Point Mode**
   - If no saved WiFi, system creates "PicoW" hotspot
   - Password: `waliori123`
   - Connect with phone/laptop

2. **Configuration Portal**
   - Navigate to `192.168.4.1` in web browser
   - Select your WiFi network
   - Enter password and submit
   - System will connect and restart

3. **Find IP Address**
   - Check your router's client list
   - Note the IP address for API access

## ✅ Quick Test

### Verify Operation

1. **Display Test**
   - Current height shows on OLED
   - WiFi icon shows connection status
   - Use rotary encoder to navigate menu

2. **Movement Test**
   - Press Up button (GPIO 27) - desk moves up
   - Press Down button (GPIO 26) - desk moves down
   - Buttons stop movement when released

3. **API Test**
   ```bash
   # Test API connectivity
   curl http://<desk-ip>/get_height
   
   # Should return: {"height": "95.5"}
   ```

### Set Presets

1. **Position 1** (Sitting)
   - Move desk to comfortable sitting height
   - Press Preset 1 button (GPIO 9) for 3 seconds
   - "Preset 1 saved" appears on display

2. **Position 2** (Standing)
   - Move to standing height
   - Press Preset 2 button (GPIO 10) for 3 seconds

3. **Position 3** (Custom)
   - Set any preferred height
   - Press Preset 3 button (GPIO 11) for 3 seconds

**Navigation Note**: Use the right-side rotary encoder (GPIO 13/14/15) for menu navigation. The left-side encoder (GPIO 20/21) provides motor position feedback only.

## 🎯 Menu Navigation

Access settings using the right-side rotary encoder (UI navigation):

**Menu → Configuration → Sleep Timer**: Set display sleep timeout
**Menu → Configuration → Reminder**: Set posture reminder interval
**Menu → WiFi → Toggle API**: Enable/disable web API
**Menu → Lock/Unlock**: Physical lock prevents all movement
**Menu → Collision Reset**: Recalibrate basic safety monitoring

**Important**: Use the right-side encoder for all menu navigation. The left-side encoder is for position feedback only.

## 🌐 Web Interface

Once WiFi is configured:

**Setup Portal**: `http://<desk-ip>/`
**API Endpoints**:
```bash
# Get current height
curl http://<desk-ip>/get_height

# Move to specific height
curl http://<desk-ip>/go?height=100.0

# Go to preset
curl http://<desk-ip>/go_preset?preset=1

# Lock desk
curl http://<desk-ip>/lock
```

## 🚀 Next Steps

**Basic Usage**: You're ready to use your smart desk!

**API Integration**: Review [REST API Reference](../api/rest-api.md)

**Hardware Details**: Check [Hardware Overview](../hardware/overview.md)

---

**🎬 Build Journey**: Experience the complete development adventure in the [YouTube documentary](https://www.youtube.com/watch?v=PKzvHBzcGJ4) to see the system in use.