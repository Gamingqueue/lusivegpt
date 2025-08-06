#!/usr/bin/env python3
"""
Key Manager for 2FA TOTP System
Allows you to add, modify, and manage keys with different usage limits
"""

import json
import pyotp
from datetime import datetime
from totp_generator import load_keys, save_keys, get_key_info

def add_key(key_name, secret=None, max_uses=1):
    """Add a new key with specified usage limit"""
    keys = load_keys()
    
    if key_name in keys:
        print(f"❌ Key '{key_name}' already exists!")
        return False
    
    if not secret:
        secret = pyotp.random_base32()
        print(f"🔑 Generated new secret: {secret}")
    
    keys[key_name] = {
        "secret": secret,
        "max_uses": max_uses,
        "usage_count": 0,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    if save_keys(keys):
        usage_text = "unlimited" if max_uses == -1 else f"{max_uses}"
        print(f"✅ Added key '{key_name}' with {usage_text} uses")
        return True
    else:
        print(f"❌ Failed to save key '{key_name}'")
        return False

def modify_key_usage(key_name, new_max_uses):
    """Modify the usage limit of an existing key"""
    keys = load_keys()
    
    if key_name not in keys:
        print(f"❌ Key '{key_name}' not found!")
        return False
    
    old_max = keys[key_name]["max_uses"]
    keys[key_name]["max_uses"] = new_max_uses
    
    if save_keys(keys):
        old_text = "unlimited" if old_max == -1 else str(old_max)
        new_text = "unlimited" if new_max_uses == -1 else str(new_max_uses)
        print(f"✅ Updated key '{key_name}' from {old_text} to {new_text} uses")
        return True
    else:
        print(f"❌ Failed to update key '{key_name}'")
        return False

def reset_key_usage(key_name):
    """Reset the usage count of a key to 0"""
    keys = load_keys()
    
    if key_name not in keys:
        print(f"❌ Key '{key_name}' not found!")
        return False
    
    old_count = keys[key_name]["usage_count"]
    keys[key_name]["usage_count"] = 0
    
    if save_keys(keys):
        print(f"✅ Reset usage count for key '{key_name}' (was {old_count}, now 0)")
        return True
    else:
        print(f"❌ Failed to reset key '{key_name}'")
        return False

def list_keys(show_secrets=False):
    """List all keys with their usage information"""
    keys = load_keys()
    
    if not keys:
        print("📝 No keys found")
        return
    
    print(f"📋 Found {len(keys)} keys:")
    print("-" * 80)
    
    for key_name, key_data in keys.items():
        max_uses = key_data.get("max_uses", 1)
        usage_count = key_data.get("usage_count", 0)
        secret = key_data.get("secret", "")
        
        if max_uses == -1:
            usage_text = f"♾️  Unlimited (used {usage_count} times)"
            status = "🟢"
        else:
            remaining = max_uses - usage_count
            if remaining > 0:
                usage_text = f"📊 {remaining}/{max_uses} uses remaining"
                status = "🟢" if remaining > 1 else "🟡"
            else:
                usage_text = f"🚫 {usage_count}/{max_uses} uses (depleted)"
                status = "🔴"
        
        print(f"{status} {key_name}")
        print(f"   {usage_text}")
        if show_secrets:
            print(f"   🔐 Secret: {secret}")
        print()

def delete_key(key_name):
    """Delete a key"""
    keys = load_keys()
    
    if key_name not in keys:
        print(f"❌ Key '{key_name}' not found!")
        return False
    
    del keys[key_name]
    
    if save_keys(keys):
        print(f"✅ Deleted key '{key_name}'")
        return True
    else:
        print(f"❌ Failed to delete key '{key_name}'")
        return False

def show_key_info(key_name):
    """Show detailed information about a specific key"""
    info = get_key_info(key_name)
    
    if not info.get('exists', False):
        print(f"❌ Key '{key_name}' not found!")
        return
    
    print(f"🔍 Key Information: {key_name}")
    print("-" * 40)
    
    max_uses = info.get('max_uses', 1)
    usage_count = info.get('usage_count', 0)
    remaining = info.get('remaining_uses', 0)
    
    print(f"📊 Usage: {usage_count} used")
    if max_uses == -1:
        print(f"♾️  Limit: Unlimited")
        print(f"✅ Status: Active (unlimited uses)")
    else:
        print(f"🎯 Limit: {max_uses} uses")
        print(f"📈 Remaining: {remaining} uses")
        if remaining > 0:
            status = "Active" if remaining > 1 else "Low (1 use left)"
            print(f"✅ Status: {status}")
        else:
            print(f"🚫 Status: Depleted")
    
    if info.get('last_used'):
        print(f"🕒 Last used: {info.get('last_used')}")
    
    if info.get('created_at'):
        print(f"📅 Created: {info.get('created_at')}")

def main():
    """Interactive key manager"""
    print("🔐 2FA Key Manager")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. List all keys")
        print("2. Add new key")
        print("3. Modify key usage limit")
        print("4. Reset key usage count")
        print("5. Show key details")
        print("6. Delete key")
        print("7. List keys with secrets")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            list_keys()
        elif choice == "2":
            key_name = input("Enter key name: ").strip()
            secret = input("Enter secret (leave empty to generate): ").strip() or None
            try:
                max_uses = input("Enter max uses (-1 for unlimited, default 1): ").strip()
                max_uses = int(max_uses) if max_uses else 1
            except ValueError:
                max_uses = 1
            add_key(key_name, secret, max_uses)
        elif choice == "3":
            key_name = input("Enter key name: ").strip()
            try:
                new_max = int(input("Enter new max uses (-1 for unlimited): ").strip())
                modify_key_usage(key_name, new_max)
            except ValueError:
                print("❌ Invalid number!")
        elif choice == "4":
            key_name = input("Enter key name: ").strip()
            reset_key_usage(key_name)
        elif choice == "5":
            key_name = input("Enter key name: ").strip()
            show_key_info(key_name)
        elif choice == "6":
            key_name = input("Enter key name: ").strip()
            confirm = input(f"Are you sure you want to delete '{key_name}'? (y/N): ").strip().lower()
            if confirm == 'y':
                delete_key(key_name)
            else:
                print("❌ Cancelled")
        elif choice == "7":
            list_keys(show_secrets=True)
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
