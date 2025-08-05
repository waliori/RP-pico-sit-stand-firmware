# Common Issues & Troubleshooting

This guide covers the most frequently encountered problems and their solutions for the Smart Sit-Stand Desk Controller.

## 🚨 Emergency Procedures

### Immediate Safety Actions

**If the desk moves unexpectedly:**
1. **Disconnect power** immediately
2. **Check for physical obstructions**
3. **Verify all connections** before reconnecting
4. **Test manually** before enabling automatic control

**If basic safety monitoring fails:**
1. **Stop using the system** immediately
2. **Check current sensor connections** and calibration
3. **Verify position encoder feedback**
4. **Test position limits** and emergency stop
5. **Note**: Advanced collision detection is under development

## 🔧 Hardware Issues

### Display Problems

#### No Display Output
**Symptoms**: OLED screen remains blank, no startup message

**Diagnostic Steps**:
```bash
# Test I2C communication
mpremote exec "from machine import I2C, Pin; i2c = I2C(0, scl=Pin(5), sda=Pin(4)); print('I2C devices:', [hex(x) for x in i2c.scan()])"
```

**Expected Output**: `I2C devices: ['0x3c']` (SH1106 address)

**Solutions**:
1. **Check power connections**:
   - OLED VCC → Pico 3V3
   - OLED GND → Pico GND
   
2. **Verify I2C wiring**:
   - OLED SDA → GPIO 4
   - OLED SCL → GPIO 5
   
3. **Test with multimeter**:
   - 3.3V present on VCC
   - Continuity on SDA/SCL lines
   
4. **Try different OLED module** (may be defective)

#### Display Shows Corruption
**Symptoms**: Garbled text, random pixels, partial display

**Common Causes**:
- Loose connections
- Interference from motor circuits
- Power supply noise

**Solutions**:
1. **Improve grounding**: Ensure solid ground connections
2. **Check power supply**: Verify stable 3.3V to display
3. **Shorten I2C cables**: Keep connections as short as possible
4. **Shield cables**: Use twisted pair or shielded cables

#### Display Dim or Flickering
**Symptoms**: Display visible but very dim or intermittent

**Solutions**:
1. **Check power supply voltage**: Should be stable 3.3V
2. **Reduce I2C frequency**: Change to 100kHz in `display.py`
3. **Check connections**: Verify SDA and SCL wiring (Pico W has internal pull-ups)

### Motor Control Issues

#### Motor Doesn't Move
**Symptoms**: No movement when buttons pressed, no motor sound

**Diagnostic Steps**:
```bash
# Test PWM output
mpremote exec "from machine import Pin, PWM; pwm = PWM(Pin(0)); pwm.freq(1000); pwm.duty_u16(32768); print('PWM active')"
```

**Check List**:
1. **Power supply**: H-bridge has adequate voltage/current
2. **PWM signals**: GPIO 0 and 1 showing PWM output
3. **Enable signals**: H-bridge enable pins connected
4. **Motor connections**: Wiring to linear actuator correct
5. **Position feedback**: Encoder properly connected

**Solutions**:
1. **Verify H-bridge wiring**:
   ```
   Pico GPIO 0 → H-Bridge IN1 (Forward PWM)
   Pico GPIO 1 → H-Bridge IN2 (Reverse PWM)
   H-Bridge OUT1/OUT2 → Motor terminals
   ```

2. **Test motor directly**: Apply DC voltage to motor terminals
3. **Check current sensor**: Ensure not causing interference
4. **Verify enable signals**: Some H-bridges need enable pins

#### Motor Runs Continuously
**Symptoms**: Motor won't stop, ignores commands

**Immediate Action**: **Disconnect power immediately**

**Diagnostic Steps**:
1. **Check encoder connections**: GPIO 20, 21 for position feedback
2. **Verify encoder signals**: Should see pulses when moved manually
3. **Test position counter**: 
   ```bash
   mpremote exec "print('Current position:', motor.counter)"
   ```

**Solutions**:
1. **Reconnect encoder**: Ensure CLK and DT are correctly wired
2. **Check encoder power**: 3.3V or 5V as required
3. **Check wiring**: Verify encoder signal connections (Pico W has internal pull-ups)
4. **Verify encoder type**: Incremental quadrature encoder required

#### Motor Jerky Movement
**Symptoms**: Stuttering, vibration, irregular speed

**Causes**:
- Poor PWM frequency
- Power supply issues
- Mechanical binding

**Solutions**:
1. **Adjust PWM frequency**: Try 16kHz (current) or 20kHz
2. **Improve power supply**: Better regulation and stable voltage
3. **Check mechanical coupling**: Ensure smooth mechanical operation
4. **Reduce acceleration**: Modify ramp-up rate in code

### Sensor Problems

#### Current Sensor Giving Wrong Readings
**Symptoms**: Collision detection too sensitive or not working

**Diagnostic Steps**:
```bash
# Test current sensor
mpremote exec "from machine import ADC; adc = ADC(28); print('Raw ADC:', adc.read_u16())"
```

**Expected Values**:
- No current: ~32768 (2.5V with ±5A sensor)
- With current: Proportional to load

**Solutions**:
1. **Check sensor type**: Ensure ACS712-30A (66mV/A sensitivity)
2. **Verify connections**:
   - VCC → 5V (not 3.3V)
   - VIOUT → GPIO 28 (may need voltage divider)
   - GND → Common ground

3. **Calibrate zero point**: 
   ```python
   # Add to acs712.py initialization
   self.zero_offset = 2.29  # Measure actual zero voltage
   ```

4. **Add filtering**: Software average over multiple readings

#### Accelerometer Not Responding
**Symptoms**: Collision detection not working, no sensor data

**Diagnostic Steps**:
```bash
# Test I2C communication
mpremote exec "from machine import I2C, Pin; i2c = I2C(1, scl=Pin(7), sda=Pin(6)); print('Devices:', [hex(x) for x in i2c.scan()])"
```

**Expected Output**: `Devices: ['0x53']` (ADXL345 address)

**Solutions**:
1. **Check I2C wiring**:
   - SDA → GPIO 6
   - SCL → GPIO 7
   - VCC → 3.3V
   - GND → Common ground

2. **Verify I2C address**: ADXL345 should appear at 0x53
3. **Test with different sensor**: Component may be defective
4. **Check I2C connections**: Verify SDA and SCL wiring (internal pull-ups enabled)

#### Position Encoder Errors
**Symptoms**: Wrong height readings, drift, jumping values

**Important**: Position feedback uses the LEFT encoder (GPIO 20/21), not the right UI encoder.

**Diagnostic Steps**:
1. **Test left encoder manually**: Turn shaft, check for pulses
2. **Verify wiring**: Left encoder CLK → GPIO 20, DT → GPIO 21
3. **Check mechanical coupling**: Left encoder should turn with motor
4. **Test position counter**:
   ```bash
   mpremote exec "print('Current encoder position:', motor.counter)"
   ```

**Solutions**:
1. **Clean left encoder contacts**: Remove dust/debris from position encoder
2. **Tighten mechanical coupling**: Ensure no slippage on motor shaft
3. **Check left encoder wiring**: Verify CLK and DT connections (internal pull-ups enabled)
4. **Check encoder type**: Incremental quadrature required
5. **Verify encoder separation**: Ensure position encoder (left) is not confused with UI encoder (right)

## 💻 Software Issues

### WiFi Connection Problems

#### Cannot Connect to Saved Networks
**Symptoms**: WiFi shows connected networks but fails to connect

**Diagnostic Steps**:
```bash
# Check saved networks
mpremote exec "import json; print(json.load(open('saved_wifi.json')))"

# Test network scanning
mpremote exec "import network; wlan = network.WLAN(network.STA_IF); wlan.active(True); print([net[0].decode() for net in wlan.scan()])"
```

**Solutions**:
1. **Verify credentials**: Delete and re-add network credentials
2. **Check signal strength**: Move closer to router
3. **Reset network config**: Delete `saved_wifi.json` file
4. **Check network compatibility**: 2.4GHz only, WPA2/WPA3

#### Access Point Mode Not Working
**Symptoms**: Cannot find "PicoW" hotspot

**Solutions**:
1. **Check AP configuration**:
   ```python
   # In wifi.py
   self.apssid = "PicoW"
   self.appassword = "waliori123"
   ```

2. **Verify AP activation**:
   ```bash
   mpremote exec "import network; ap = network.WLAN(network.AP_IF); ap.active(True); print('AP active:', ap.active())"
   ```

3. **Try different device**: Some phones/laptops have WiFi compatibility issues

#### Web Interface Not Accessible
**Symptoms**: Cannot reach 192.168.4.1 or device IP

**Diagnostic Steps**:
1. **Ping test**: `ping 192.168.4.1` (AP mode) or device IP
2. **Port scan**: `nmap -p 80 <device-ip>`
3. **Check web server**: 
   ```bash
   mpremote exec "print('Web server running:', wifi.server)"
   ```

**Solutions**:
1. **Restart web server**: Power cycle device
2. **Check firewall**: Disable temporarily on client device
3. **Try different browser**: Some browsers cache aggressively
4. **Use IP address**: Instead of hostname

### Menu System Issues

#### Rotary Encoder Not Working
**Symptoms**: Cannot navigate menu, encoder doesn't respond

**Important**: This system uses TWO separate rotary encoders:
- **Right Encoder** (GPIO 13/14/15): UI navigation with button
- **Left Encoder** (GPIO 20/21): Motor position feedback only

**Diagnostic Steps for UI Navigation (Right Encoder)**:
```bash
# Test UI encoder inputs
mpremote exec "from machine import Pin; clk = Pin(15, Pin.IN, Pin.PULL_UP); dt = Pin(14, Pin.IN, Pin.PULL_UP); sw = Pin(13, Pin.IN, Pin.PULL_UP); print('UI Encoder - CLK:', clk.value(), 'DT:', dt.value(), 'SW:', sw.value())"
```

**Diagnostic Steps for Position Feedback (Left Encoder)**:
```bash
# Test position encoder inputs
mpremote exec "from machine import Pin; clk = Pin(20, Pin.IN, Pin.PULL_UP); dt = Pin(21, Pin.IN, Pin.PULL_UP); print('Position Encoder - CLK:', clk.value(), 'DT:', dt.value())"
```

**Expected Values**:
- All should read 1 (high) when not pressed/turned
- Values should change when encoder moved

**Solutions**:
1. **Check UI encoder wiring (right side)**:
   - CLK → GPIO 15
   - DT → GPIO 14  
   - SW → GPIO 13

2. **Check position encoder wiring (left side)**:
   - CLK → GPIO 20
   - DT → GPIO 21

3. **Enable pull-ups**: Already done in code, verify hardware
4. **Test encoders mechanically**: Both should click when turned
5. **Try different encoders**: Components may be defective

#### Menu Freezes or Unresponsive
**Symptoms**: Display shows menu but doesn't respond to inputs

**Solutions**:
1. **Restart system**: Power cycle device
2. **Check thread locks**: May be deadlocked
3. **Clear display lock**:
   ```bash
   mpremote exec "import _thread; sLock = _thread.allocate_lock(); sLock.release()"
   ```

### Calibration Problems

#### Height Calibration Fails
**Symptoms**: Cannot complete calibration, wrong height values

**Solutions**:
1. **Clear previous calibration**:
   ```bash
   # Delete configuration files
   mpremote fs rm settings.json
   mpremote fs rm state.json
   ```

2. **Manual encoder test**:
   ```bash
   mpremote exec "print('Encoder position:', motor.counter)"
   ```

3. **Check encoder range**: Should change significantly between limits

#### Basic Safety Monitoring Issues
**Symptoms**: Unexpected stops, false safety triggers

**Solutions**:
1. **Check current sensor calibration**: Verify ACS712 connections and zero point
2. **Verify position limits**: Ensure encoder feedback is accurate
3. **Test individual sensors**: Isolate and test each safety component
4. **Update configuration**: Adjust safety thresholds in settings.json
5. **Future Enhancement**: Advanced PCA-based collision detection is under development

## 🔍 Diagnostic Tools

### Built-in Diagnostics

#### System Status Check
```bash
mpremote exec "
import os, sys, gc
print('MicroPython:', sys.implementation)
print('Available memory:', gc.mem_free())
print('Files:', os.listdir())
print('System ready')
"
```

#### Sensor Reading Test
```bash
mpremote exec "
# Test all sensors
from machine import I2C, Pin, ADC
import accelerometer, acs712

# I2C devices
i2c0 = I2C(0, scl=Pin(5), sda=Pin(4))
i2c1 = I2C(1, scl=Pin(7), sda=Pin(6))
print('I2C0 devices:', [hex(x) for x in i2c0.scan()])
print('I2C1 devices:', [hex(x) for x in i2c1.scan()])

# Current sensor
adc = ADC(28)
print('Current sensor raw:', adc.read_u16())

# Accelerometer
try:
    accel = accelerometer.Accelerometer(Pin(6), Pin(7), 400000)
    print('Accelerometer:', accel.read_accel_data())
except:
    print('Accelerometer error')
"
```

#### Network Diagnostics
```bash
mpremote exec "
import network
wlan = network.WLAN(network.STA_IF)
print('WiFi active:', wlan.active())
print('Connected:', wlan.isconnected())
if wlan.isconnected():
    print('IP config:', wlan.ifconfig())
print('Scan results:', len(wlan.scan()), 'networks found')
"
```

### External Tools

#### Network Analysis
```bash
# Find device on network
nmap -sn 192.168.1.0/24 | grep -B2 "Raspberry Pi"

# Port scan
nmap -p 80,8080 <device-ip>

# HTTP test
curl -v http://<device-ip>/get_height
```

#### Serial Monitoring
```bash
# Linux/Mac
screen /dev/ttyACM0 115200

# Windows (PowerShell)
python -m serial.tools.miniterm COM3 115200

# View continuous output
tail -f /dev/ttyACM0
```

## 🛠️ Recovery Procedures

### Factory Reset

#### Software Reset
```bash
# Delete all configuration files
mpremote fs rm settings.json
mpremote fs rm presets.json  
mpremote fs rm saved_wifi.json
mpremote fs rm state.json

# Restart system
mpremote reset
```

#### Complete Reinstall
```bash
# Backup any custom files first
mpremote fs cp settings.json settings_backup.json

# Remove all files
mpremote fs rm *.py
mpremote fs rm *.json

# Re-upload firmware
mpremote fs cp *.py :

# Reset and restart
mpremote reset
```

#### Hardware Reset
1. **Hold BOOTSEL button** while connecting USB
2. **Copy UF2 firmware** to mounted drive
3. **Reconnect normally** and re-upload code

### Emergency Safe Mode

If system becomes completely unresponsive:

1. **Create minimal main.py**:
   ```python
   # minimal_main.py
   print("Safe mode - system ready")
   from machine import Pin
   led = Pin("LED", Pin.OUT)
   led.on()  # LED on indicates safe mode
   ```

2. **Upload and test**:
   ```bash
   mpremote fs cp minimal_main.py main.py
   mpremote reset
   ```

3. **Gradually add functionality** back until issue is identified

## 📞 Getting Help

### Information to Collect

Before seeking help, gather:

1. **Hardware configuration**: Components used, wiring details
2. **Software version**: Git commit hash or download date
3. **Error messages**: Complete error text from console
4. **System status**: Output of diagnostic commands above
5. **Steps to reproduce**: Exact sequence that causes issue

### Debug Logs

Enable detailed logging:
```python
# Add to main.py
DEBUG = True

def log_debug(message):
    if DEBUG:
        print(f"[{time.ticks_ms()}] DEBUG: {message}")
```

### Community Support

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share solutions
- **Documentation**: Check other wiki pages for detailed info

### Professional Support

For commercial or safety-critical applications:
- Consult qualified electricians for power systems
- Consider professional mechanical integration
- Implement additional safety systems as required

---

**Remember**: When in doubt, prioritize safety. Disconnect power and seek help rather than risk injury or equipment damage.