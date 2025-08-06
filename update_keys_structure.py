import json

def update_keys_structure():
    """Update keys structure to support usage limits"""
    
    # Read current keys
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    
    # Convert structure
    updated_keys = {}
    
    for key, data in keys.items():
        # Convert old boolean 'used' to new usage count system
        if data.get('used', False):
            # If key was already used, set usage_count to max_uses
            updated_keys[key] = {
                "secret": data["secret"],
                "max_uses": 1,  # Default to 1 use for existing keys
                "usage_count": 1,  # Already used
                "created_at": "2025-01-01T00:00:00Z"  # Default timestamp
            }
        else:
            # If key was not used, set usage_count to 0
            updated_keys[key] = {
                "secret": data["secret"],
                "max_uses": 1,  # Default to 1 use for existing keys
                "usage_count": 0,  # Not used yet
                "created_at": "2025-01-01T00:00:00Z"  # Default timestamp
            }
    
    # Add some example keys with different usage limits
    updated_keys["MULTI_USE_KEY_001"] = {
        "secret": "JBSWY3DPEHPK3PXP",
        "max_uses": 5,  # Can be used 5 times
        "usage_count": 0,
        "created_at": "2025-01-01T00:00:00Z"
    }
    
    updated_keys["UNLIMITED_KEY_001"] = {
        "secret": "GAXSW23XPQ4B2CZR",
        "max_uses": -1,  # Unlimited uses (-1 means unlimited)
        "usage_count": 0,
        "created_at": "2025-01-01T00:00:00Z"
    }
    
    # Save updated structure
    with open('keys.json', 'w') as f:
        json.dump(updated_keys, f, indent=2)
    
    print(f"Updated {len(keys)} keys to new structure")
    print("Added example keys:")
    print("- MULTI_USE_KEY_001: Can be used 5 times")
    print("- UNLIMITED_KEY_001: Unlimited uses")
    
    # Show first few keys as examples
    print("\nSample updated structure:")
    count = 0
    for key, data in updated_keys.items():
        if count < 3:
            print(f"Key: {key}")
            print(f"  Secret: {data['secret']}")
            print(f"  Max Uses: {data['max_uses']}")
            print(f"  Usage Count: {data['usage_count']}")
            print(f"  Available Uses: {'Unlimited' if data['max_uses'] == -1 else data['max_uses'] - data['usage_count']}")
            print("---")
            count += 1
        else:
            break

if __name__ == "__main__":
    update_keys_structure()
