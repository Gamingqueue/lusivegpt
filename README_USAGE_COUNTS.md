# 2FA TOTP Generator with Usage Count Management

This system has been enhanced to support configurable usage limits for each key, allowing you to control how many times each key can be used to generate TOTP codes.

## 🆕 New Features

### Usage Count System
- **Single Use Keys**: Traditional one-time use keys (default)
- **Multi-Use Keys**: Keys that can be used a specific number of times
- **Unlimited Keys**: Keys with no usage restrictions

### Key Structure
Each key now has the following properties:
```json
{
  "KEY_NAME": {
    "secret": "BASE32_SECRET",
    "max_uses": 5,           // -1 for unlimited, positive number for limit
    "usage_count": 2,        // How many times it's been used
    "created_at": "2025-01-01T00:00:00Z",
    "last_used": "2025-01-01T12:00:00Z"
  }
}
```

## 🔧 Usage Examples

### Test Keys Available
1. **MULTI_USE_KEY_001**: Can be used 5 times
2. **UNLIMITED_KEY_001**: Unlimited uses
3. **TEST_KEY_2FA_001**: Your custom key (single use)

### API Responses
The API now returns usage information:

```json
{
  "code": "123456",
  "success": true,
  "usage_info": {
    "max_uses": 5,
    "usage_count": 2,
    "remaining_uses": 3
  }
}
```

For unlimited keys:
```json
{
  "usage_info": {
    "max_uses": -1,
    "usage_count": 15,
    "remaining_uses": "unlimited"
  }
}
```

## 🛠️ Key Management

### Using the Key Manager
Run the interactive key manager:
```bash
python key_manager.py
```

### Key Manager Features
1. **List Keys**: View all keys with their usage status
2. **Add New Key**: Create keys with custom usage limits
3. **Modify Usage Limit**: Change how many times a key can be used
4. **Reset Usage Count**: Reset a key's usage count to 0
5. **Show Key Details**: View detailed information about a specific key
6. **Delete Key**: Remove a key from the system

### Command Line Examples

#### Add a new key with 10 uses:
```python
from key_manager import add_key
add_key("MY_KEY_001", max_uses=10)
```

#### Add unlimited use key:
```python
add_key("UNLIMITED_KEY_002", max_uses=-1)
```

#### Reset a key's usage count:
```python
from key_manager import reset_key_usage
reset_key_usage("MULTI_USE_KEY_001")
```

#### Modify usage limit:
```python
from key_manager import modify_key_usage
modify_key_usage("MY_KEY_001", 20)  # Change to 20 uses
```

## 🌐 Web Interface

The web interface now displays usage information when generating codes:

- **Single Use**: Shows "1 use remaining" before use, then key becomes invalid
- **Multi-Use**: Shows "X uses remaining (Y/Z used)" 
- **Unlimited**: Shows "Unlimited uses (Used X times)"

## 📊 Key Status Indicators

- 🟢 **Green**: Key has multiple uses remaining or unlimited
- 🟡 **Yellow**: Key has 1 use remaining
- 🔴 **Red**: Key is depleted (no uses remaining)
- ♾️ **Infinity**: Unlimited use key
- 📊 **Chart**: Multi-use key with remaining uses

## 🔒 Security Features

1. **One-time validation**: Each key validation checks current usage status
2. **Atomic updates**: Usage counts are updated atomically
3. **Timestamp tracking**: Last used time is recorded for each key
4. **Usage history**: Complete usage tracking for audit purposes

## 🚀 API Endpoints

### New Endpoint: `/key-info`
Get detailed information about a key:
```bash
curl -X POST http://localhost:8000/key-info \
  -H "Content-Type: application/json" \
  -d '{"key": "MULTI_USE_KEY_001"}'
```

Response:
```json
{
  "exists": true,
  "max_uses": 5,
  "usage_count": 2,
  "remaining_uses": 3,
  "is_valid": true,
  "last_used": "2025-08-06T06:04:47.841583Z",
  "created_at": "2025-01-01T00:00:00Z"
}
```

### Enhanced Endpoints
- `/validate-key`: Now returns usage information
- `/get-code`: Returns updated usage info after code generation

## 📝 Migration

Your existing keys have been automatically migrated:
- All existing keys default to `max_uses: 1` (single use)
- Previously used keys are marked with `usage_count: 1`
- Unused keys have `usage_count: 0`

## 🎯 Use Cases

1. **Personal Use**: Single-use keys for maximum security
2. **Team Access**: Multi-use keys for shared access with limits
3. **Service Accounts**: Unlimited keys for automated systems
4. **Testing**: Resettable keys for development and testing
5. **Temporary Access**: Time-limited keys with usage counts

## 🔧 Configuration

You can easily customize the default behavior by modifying the key structure or using the key manager to set up keys according to your needs.
