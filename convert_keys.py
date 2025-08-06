import json
import pyotp

def convert_keys():
    """Convert old keys format to new format with TOTP secrets"""
    
    # Read old keys
    with open('keys_backup.json', 'r') as f:
        old_keys = json.load(f)
    
    # Convert to new format
    new_keys = {}
    
    for key in old_keys:
        # Generate a unique TOTP secret for each key
        secret = pyotp.random_base32()
        new_keys[key] = {
            "secret": secret,
            "used": False
        }
    
    # Save new format
    with open('keys.json', 'w') as f:
        json.dump(new_keys, f, indent=2)
    
    print(f"Converted {len(old_keys)} keys to new format")
    print("Sample keys with their secrets:")
    
    # Show first 3 keys as examples
    count = 0
    for key, data in new_keys.items():
        if count < 3:
            print(f"Key: {key}")
            print(f"Secret: {data['secret']}")
            print(f"Used: {data['used']}")
            print("---")
            count += 1
        else:
            break

if __name__ == "__main__":
    convert_keys()
