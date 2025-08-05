# Smart Sit-Stand Desk Controller - Documentation

Documentation for the Smart Sit-Stand Desk Controller project built with Raspberry Pi Pico W and MicroPython.

🎬 **[Watch the Build Journey](https://www.youtube.com/watch?v=PKzvHBzcGJ4)** - Experience the development adventure and see the finished system in action.

⚠️ **Project Status**: Advanced collision detection features are currently Work In Progress as part of the [Micropython sit/stand smart table project](https://github.com/users/waliori/projects/1).

## 📋 Documentation

### Hardware
- **[Hardware Overview](hardware/overview.md)** - Components and pin assignments
- **[Bill of Materials](hardware/bom.md)** - Electronic components list
- **[3D Models & CAD Files](https://cad.onshape.com/documents/f9483c31494feda60f507100/w/67832ca84d886d2bfa4006b1/e/62aed646cd76d0a16e7ccfc5?renderMode=0&uiState=68916ac8ffbe3d6103e400d4)** - Open-source CAD models

### Software  
- **[System Architecture](software/architecture.md)** - Software design and modules

### API
- **[REST API Reference](api/rest-api.md)** - HTTP API documentation

### Setup
- **[Quick Start Guide](setup/quick-start.md)** - Setup instructions

## 🎯 Quick Navigation

### For New Users
1. Check [Hardware Overview](hardware/overview.md) for components
2. Follow [Quick Start Guide](setup/quick-start.md) for setup
3. Use [REST API Reference](api/rest-api.md) for control

### For Developers
1. Review [System Architecture](software/architecture.md)
2. Study [REST API Reference](api/rest-api.md)

## 📋 Project Overview

This documentation covers a sit-stand desk controller featuring:

- **Basic Safety**: Position limits, current monitoring
- **WiFi Control**: Web interface and REST API  
- **OLED Display**: Menu navigation with rotary encoder
- **Position Tracking**: Encoder feedback
- **Future: Advanced Collision Detection** ⚠️ PCA-based (under development)

### 🎬 Build Story

Experience the complete development journey in the [YouTube documentary](https://www.youtube.com/watch?v=PKzvHBzcGJ4).

## 📈 Project Status

### ✅ Completed Features
- Motor control and position tracking
- WiFi connectivity and web interface
- Basic safety monitoring (current sensing, position limits)
- OLED display with menu navigation
- RESTful API for remote control

### 🚧 Work In Progress
- **Advanced Collision Detection**: PCA-based algorithm implementation

### 🔗 Project Links
- **🎬 Build Documentary**: https://www.youtube.com/watch?v=PKzvHBzcGJ4
- **Main Project Board**: https://github.com/users/waliori/projects/1
- **Repository**: https://github.com/waliori/RP-pico-sit-stand-firmware

---

**📞 Support**: [GitHub Issues](https://github.com/waliori/RP-pico-sit-stand-firmware/issues)