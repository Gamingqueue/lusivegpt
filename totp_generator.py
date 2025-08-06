import os
import json
import pyotp
from typing import Tuple, Optional, Dict, Any
from datetime import datetime

def load_keys():
    """Load keys from keys.json file"""
    try:
        with open('keys.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: keys.json file not found")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in keys.json")
        return {}

def save_keys(keys):
    """Save keys to keys.json file"""
    try:
        with open('keys.json', 'w') as f:
            json.dump(keys, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving keys: {e}")
        return False

def generate_totp_code(user_key: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generate TOTP code for the given user key and increment usage count
    
    Args:
        user_key: The access key provided by the user
        
    Returns:
        Tuple of (code, error_message). If successful, returns (code, None).
        If failed, returns (None, error_message).
    """
    try:
        keys = load_keys()
        
        # Check if key exists
        if user_key not in keys:
            return None, "Invalid key provided"
        
        key_data = keys[user_key]
        max_uses = key_data.get("max_uses", 1)
        usage_count = key_data.get("usage_count", 0)
        
        # Check if key has reached usage limit (unless unlimited)
        if max_uses != -1 and usage_count >= max_uses:
            remaining = max_uses - usage_count
            return None, f"Key has reached its usage limit ({usage_count}/{max_uses} uses)"
        
        # Get the secret for TOTP generation
        secret = key_data.get("secret")
        if not secret:
            return None, "No secret found for this key"
        
        # Generate TOTP code
        totp = pyotp.TOTP(secret)
        code = totp.now()
        
        # Increment usage count
        keys[user_key]["usage_count"] = usage_count + 1
        
        # Add last_used timestamp
        keys[user_key]["last_used"] = datetime.utcnow().isoformat() + "Z"
        
        # Save updated keys
        if not save_keys(keys):
            return None, "Failed to update key usage count"
        
        return code, None
        
    except Exception as e:
        return None, f"Error generating TOTP code: {str(e)}"

def validate_key(user_key: str) -> bool:
    """
    Validate if a key exists and has remaining uses
    
    Args:
        user_key: The access key to validate
        
    Returns:
        True if key is valid and has remaining uses, False otherwise
    """
    try:
        keys = load_keys()
        
        # Check if key exists
        if user_key not in keys:
            return False
        
        key_data = keys[user_key]
        max_uses = key_data.get("max_uses", 1)
        usage_count = key_data.get("usage_count", 0)
        
        # Check if key has remaining uses
        if max_uses == -1:  # Unlimited uses
            return True
        elif usage_count < max_uses:  # Has remaining uses
            return True
        else:  # No remaining uses
            return False
        
    except Exception as e:
        print(f"Error validating key: {e}")
        return False

def get_key_info(user_key: str) -> Dict[str, Any]:
    """
    Get detailed information about a key
    
    Args:
        user_key: The access key to get info for
        
    Returns:
        Dictionary with key information
    """
    try:
        keys = load_keys()
        
        if user_key not in keys:
            return {"exists": False}
        
        key_data = keys[user_key]
        max_uses = key_data.get("max_uses", 1)
        usage_count = key_data.get("usage_count", 0)
        
        return {
            "exists": True,
            "max_uses": max_uses,
            "usage_count": usage_count,
            "remaining_uses": "unlimited" if max_uses == -1 else max_uses - usage_count,
            "is_valid": validate_key(user_key),
            "last_used": key_data.get("last_used"),
            "created_at": key_data.get("created_at")
        }
        
    except Exception as e:
        return {"exists": False, "error": str(e)}

def generate_random_secret() -> str:
    """Generate a random base32 secret for TOTP"""
    return pyotp.random_base32()

def add_new_key(access_key: str, secret: str = None) -> bool:
    """
    Add a new access key with TOTP secret
    
    Args:
        access_key: The access key to add
        secret: Optional TOTP secret. If not provided, generates random one
        
    Returns:
        True if successful, False otherwise
    """
    try:
        keys = load_keys()
        
        if access_key in keys:
            print(f"Key {access_key} already exists")
            return False
        
        if not secret:
            secret = generate_random_secret()
        
        keys[access_key] = {
            "secret": secret,
            "used": False
        }
        
        return save_keys(keys)
        
    except Exception as e:
        print(f"Error adding new key: {e}")
        return False

if __name__ == "__main__":
    # Test the functions
    print("Testing TOTP Generator...")
    
    # Example usage
    test_key = "TEST_KEY_123"
    test_secret = generate_random_secret()
    
    print(f"Generated secret: {test_secret}")
    
    # Add test key
    if add_new_key(test_key, test_secret):
        print(f"Added test key: {test_key}")
        
        # Validate key
        if validate_key(test_key):
            print("Key validation: PASSED")
            
            # Generate code
            code, error = generate_totp_code(test_key)
            if code:
                print(f"Generated TOTP code: {code}")
            else:
                print(f"Error: {error}")
        else:
            print("Key validation: FAILED")
