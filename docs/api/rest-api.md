# REST API Reference

Complete API documentation for the Smart Sit-Stand Desk Controller. All endpoints support CORS for cross-origin requests.

## 🌐 Base URL

```
http://<pico-ip-address>/
```

Replace `<pico-ip-address>` with your Pico W's IP address on your network.

## 📋 Available Endpoints

### Status & Information

#### Get Current Height
```http
GET /get_height
```

**Description**: Returns the current desk height in real-world units.

**Response:**
```json
{"height": "95.5"}
```

#### Get Min/Max Heights
```http
GET /get_minmax
```

**Description**: Returns the configured minimum and maximum height limits.

**Response:**
```json
{"min": 72.0, "max": 120.0}
```

#### Get Preset Heights
```http
GET /get_presets
```

**Description**: Returns all configured preset heights.

**Response:**
```json
["1: 95.5", "2: 110.0", "3: 115.2"]
```

#### Check Lock Status
```http
GET /islocked
```

**Description**: Returns whether the desk is currently locked.

**Response:**
```json
{"locked": false}
```

### Movement Controls

#### Move Up
```http
GET /forward
```

**Description**: Starts moving the desk upward.

**Response:**
```json
{"status": "ok"}
```

**Note**: Returns `{"status": "nok"}` if desk is locked.

#### Move Down
```http
GET /backward
```

**Description**: Starts moving the desk downward.

**Response:**
```json
{"status": "ok"}
```

**Note**: Returns `{"status": "nok"}` if desk is locked.

#### Stop Movement
```http
GET /stop
```

**Description**: Immediately stops any desk movement.

**Response:**
```json
{"status": "ok"}
```

### Position Control

#### Go to Specific Height
```http
GET /go?height=100.5
```

**Parameters:**
- `height` (required): Target height in real-world units (float)

**Description**: Moves desk to the specified height.

**Response:**
```json
{"status": "ok"}
```

#### Go to Preset
```http
GET /go_preset?preset=1
```

**Parameters:**
- `preset` (required): Preset number (1, 2, or 3)

**Description**: Moves desk to the specified preset position.

**Response:**
```json
{"status": "ok"}
```

**Note**: Returns `{"status": "nok"}` if preset doesn't exist.

### Security Controls

#### Lock Desk
```http
GET /lock
```

**Description**: Locks the desk to prevent all movement.

**Response:**
```json
{"status": "ok"}
```

#### Unlock Desk
```http
GET /unlock
```

**Description**: Unlocks the desk to allow movement.

**Response:**
```json
{"status": "ok"}
```

### Configuration

#### Set Minimum Height
```http
GET /set_min?min=70.0
```

**Parameters:**
- `min` (required): New minimum height limit (float)

**Description**: Updates the minimum height limit.

**Response:**
```json
{"status": "ok"}
```

#### Set Maximum Height
```http
GET /set_max?max=125.0
```

**Parameters:**
- `max` (required): New maximum height limit (float)

**Description**: Updates the maximum height limit.

**Response:**
```json
{"status": "ok"}
```

## 🔧 Response Format

All API endpoints return JSON responses with consistent formatting.

### Success Response
```json
{
  "status": "ok",
  "data": "response_data"
}
```

### Error Response
```json
{
  "status": "nok",
  "error": "Description of error"
}
```

### HTTP Headers

All responses include CORS headers:
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: *
```

## 📱 Integration Examples

### JavaScript/Fetch API
```javascript
// Get current height
const response = await fetch('http://192.168.1.100/get_height');
const data = await response.json();
console.log('Current height:', data.height);

// Move to specific height
await fetch('http://192.168.1.100/go?height=110.0');

// Go to preset 1
await fetch('http://192.168.1.100/go_preset?preset=1');
```

### Python Requests
```python
import requests

# Get current height
response = requests.get('http://192.168.1.100/get_height')
height = response.json()['height']
print(f'Current height: {height}')

# Move desk up
requests.get('http://192.168.1.100/forward')

# Stop movement after delay
time.sleep(2)
requests.get('http://192.168.1.100/stop')
```

### cURL Commands
```bash
# Get current height
curl http://192.168.1.100/get_height

# Move to sitting height
curl "http://192.168.1.100/go?height=95.0"

# Lock desk
curl http://192.168.1.100/lock

# Check if locked
curl http://192.168.1.100/islocked
```

## 🔒 Security Considerations

### Physical Lock
The `/lock` endpoint provides a software lock that prevents all movement commands. When locked:
- Movement endpoints (`/forward`, `/backward`, `/go`, `/go_preset`) return `{"status": "nok"}`
- Configuration changes are still allowed
- The lock persists across system restarts

### Network Security
- API is accessible to all devices on the local network
- No authentication required (designed for home/office use)
- Consider network-level security (VPN, firewall rules) for enhanced protection

## ⚠️ Important Notes

### Safety
- Always verify desk response before issuing multiple commands
- Use `/stop` endpoint for emergency stops
- Physical buttons override API commands
- Height limits are enforced in software

### Rate Limiting
- No built-in rate limiting
- Avoid rapid successive calls to prevent system overload
- Allow movement commands to complete before issuing new ones

### Error Handling
- Always check response status (`"ok"` vs `"nok"`)
- Handle network timeouts gracefully
- Implement retry logic for critical operations

---

**📞 Support**: For API issues or feature requests, use [GitHub Issues](https://github.com/waliori/RP-pico-sit-stand-firmware/issues)