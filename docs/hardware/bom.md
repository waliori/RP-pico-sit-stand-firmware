# Bill of Materials (BOM)

Electronic components list for building the Smart Sit-Stand Desk Controller. Quantities reflect actual parts used in the project.

## 📋 Electronic Components List

### Core Electronics

| Component | Description | Quantity Used | Notes |
|-----------|-------------|---------------|--------|
| **Raspberry Pi Pico W** | Main microcontroller with WiFi | 1 | Official distributor recommended |
| **BTS7960B H-Bridge** | Motor driver module | 1 | High current capability |
| **37GB555 Geared Motor** | 12V 180RPM DC motor with encoder | 1 | High torque gear reducer |
| **ACS712-30A** | Current sensor module | 1 | 30A Hall effect sensor |
| **ADXL345** | 3-axis accelerometer | 1 | I2C interface |
| **SH1106 OLED** | 128x64 monochrome display | 1 | I2C interface |

### Power & Electrical

| Component | Description | Quantity Used | Notes |
|-----------|-------------|---------------|--------|
| **12V Power Supply** | Main power for motor | 1 | Motor power only |
| **3.3V Regulator** | Powers all electronics | 1 | From 12V to 3.3V for logic |
| **Power Connectors** | Various DC connectors | As needed | Power distribution |

### User Interface

| Component | Description | Quantity Used | Notes |
|-----------|-------------|---------------|--------|
| **KY-040 Rotary Encoder** | 360° rotary encoder with button | 1 | UI navigation (right side) |
| **KY-040 Rotary Encoder** | 360° rotary encoder (no button) | 1 | Motor position feedback (left side) |
| **Tactile Buttons** | Push buttons for controls | 5 | Up, Down, Preset 1-3 |
| **Mini Rocker Switch** | 2-pin 10x15mm power switch | 1 | ON/OFF functionality |

### Mechanical Components

| Component | Description | Quantity Used | Notes |
|-----------|-------------|---------------|--------|
| **Shaft Coupling** | 6mm to 7mm flexible coupler | 1 | D25L30 plum jaw spider |
| **Deep Groove Bearings** | 6000ZZ ball bearings | 2 | High quality |

### Additional Electronics

| Component | Description | Quantity Used | Notes |
|-----------|-------------|---------------|--------|
| **Buzzer** | Piezo buzzer (PWM driven) | 1 | Audio feedback |
| **Vibration Motor** | Coin vibration motor 3V | 1 | Haptic feedback |
| **Connection Wires** | Various connection wires | As needed | Prototyping connections |
| **Prototyping Board** | PCB or breadboard | 1 | For permanent assembly |

**Note**: This project uses the Pico W's internal pull-up resistors - no external resistors or capacitors needed for basic operation.

## 💰 Cost Information

**Note**: Costs vary significantly by supplier, region, shipping, and bulk purchasing. The components listed represent the actual electronic parts used in this project. Total project costs will vary based on:

- **Supplier selection** (AliExpress vs Amazon vs DigiKey)
- **Shipping costs** and delivery time preferences
- **Bulk vs individual** purchasing decisions
- **Regional pricing** variations
- **3D printing and mechanical components** (not included in electronics BOM - see CAD files below)
- **Tools and assembly materials** (solder, heat shrink, etc.)

## 🛒 Sourcing Recommendations

### Primary Suppliers

#### Budget-Friendly Options
- **AliExpress**: Best prices for most components (2-4 week shipping)
- **Banggood**: Good selection and reasonable shipping times
- **DHgate**: Bulk quantities available

#### Faster Shipping Options
- **Amazon**: 1-2 day shipping, higher prices
- **DigiKey/Mouser**: Professional grade, excellent for critical components
- **Adafruit/SparkFun**: High-quality breakout boards, educational support

### Regional Suppliers

#### North America
- **DigiKey** (Minnesota, USA)
- **Mouser Electronics** (Texas, USA)
- **Adafruit** (New York, USA)
- **SparkFun** (Colorado, USA)

#### Europe
- **Farnell** (UK/EU)
- **RS Components** (EU)
- **Conrad Electronic** (Germany)

#### Asia-Pacific
- **Element14** (Australia/Asia)
- **Seeed Studio** (China)
- **DFRobot** (China)

## 🔧 Sourcing Strategy

### Phase 1: Essential Components
Start with core electronics to verify functionality:
1. Raspberry Pi Pico W
2. H-Bridge motor driver
3. Power supply and buck converters
4. OLED display
5. Basic breadboard setup

### Phase 2: Motor System
Add mechanical components:
1. Geared motor
2. Shaft coupling
3. Bearings
4. Mounting hardware

### Phase 3: User Interface
Complete the control system:
1. Rotary encoders
2. Mechanical switches
3. Buttons and enclosure

### Phase 4: Sensors & Safety
Final safety and monitoring:
1. Current sensor
2. Accelerometer
3. Additional sensors as needed

## 📦 Bulk Purchase Recommendations

### Typical Purchasing Considerations
- **Resistors**: Often sold in assorted packs
- **Capacitors**: Common values available in variety packs
- **Jumper Wires**: Usually sold in multi-packs
- **Connectors**: May need to buy more than required for project

### Individual Component Items
- **Raspberry Pi Pico W**: From authorized distributor
- **Motor**: Specific torque/speed requirements
- **Power Supply**: Match local electrical standards
- **Coupling**: Exact shaft size matching

## ⚠️ Important Notes

### Safety Considerations
- **Power Supply**: Ensure proper electrical isolation
- **Motor Current**: Verify H-bridge can handle motor load
- **Heat Dissipation**: Consider cooling for high-power components
- **Enclosure**: Use fire-resistant materials for electronics (3D printable designs available)

### Quality Recommendations
- **Critical Components**: Buy from reputable suppliers
  - Raspberry Pi Pico W (avoid clones)
  - Power supply (certified safety ratings)
  - Motor driver (genuine BTS7960B)
- **Test Components**: Before final assembly
- **Backup Parts**: Keep spares of critical components

### Purchasing Tips
1. **Compare Suppliers**: Prices vary significantly between vendors
2. **Check Reviews**: Verify component quality, especially for critical parts
3. **Consider Shipping**: Factor delivery costs and timeframes
4. **Local Availability**: Check electronics stores for immediate needs

## 📋 Pre-Assembly Checklist

Before starting your build:

- [ ] **All components received** and verified against BOM
- [ ] **Power supply tested** and voltage verified
- [ ] **Workspace prepared** with proper tools
- [ ] **Documentation reviewed** including wiring diagrams
- [ ] **Safety equipment ready** (safety glasses, proper lighting)
- [ ] **Backup components** for critical parts available

## 🔗 Useful Links

### 🎨 **3D Models & CAD Files** (Fully Open Source)
- **📐 Complete CAD Models**: [OnShape CAD Document](https://cad.onshape.com/documents/f9483c31494feda60f507100/w/67832ca84d886d2bfa4006b1/e/62aed646cd76d0a16e7ccfc5?renderMode=0&uiState=68916ac8ffbe3d6103e400d4) - Fully editable CAD format
- **🖨️ 3D Printable Parts**: All enclosures, mounts, and brackets available in native CAD format
- **📝 Mechanical Drawings**: Dimensions and tolerances included in CAD

### 📚 Additional Resources
- **Schematic Diagrams**: [Circuit Diagrams](circuit-diagrams.md)
- **Assembly Guide**: [Hardware Assembly](assembly.md)
- **Build Video**: [🎬 YouTube Documentary](https://www.youtube.com/watch?v=PKzvHBzcGJ4)

---

**💡 Tip**: Start with a breadboard prototype to verify all connections before committing to a permanent PCB or enclosure assembly. All 3D printable parts are available in the OnShape CAD document above.

**⚠️ Important**: This BOM lists only electronic components actually used in the project. Costs are not provided as they vary significantly by supplier, region, and purchasing decisions. Always verify current pricing and component specifications before ordering.