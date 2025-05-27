#!/usr/bin/env python3
"""
Test script to verify both local and Railway configurations work properly.
"""
import os
import sys

def load_env_file(filename):
    """Load environment variables from file"""
    env_vars = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
        return env_vars
    except FileNotFoundError:
        print(f"❌ Environment file {filename} not found")
        return {}

def test_config(config_name, env_file):
    """Test a specific configuration"""
    print(f"\n🧪 Testing {config_name} Configuration...")
    print("=" * 50)
    
    env_vars = load_env_file(env_file)
    if not env_vars:
        return False
    
    # Check required variables
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'ADDONS_PATH']
    missing_vars = []
    
    for var in required_vars:
        if var in env_vars:
            print(f"✅ {var}: {env_vars[var]}")
        else:
            print(f"❌ {var}: Missing")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing variables: {missing_vars}")
        return False
    else:
        print(f"\n✅ {config_name} configuration is complete!")
        return True

def main():
    print("🔍 Odoo Configuration Tester")
    print("============================")
    
    # Test local configuration (files are in parent directory)
    local_ok = test_config("LOCAL", "../local.env")
    
    # Test Railway configuration  
    railway_ok = test_config("RAILWAY", "../railway.env")
    
    print("\n📊 Summary:")
    print("=" * 20)
    print(f"Local Config:   {'✅ PASS' if local_ok else '❌ FAIL'}")
    print(f"Railway Config: {'✅ PASS' if railway_ok else '❌ FAIL'}")
    
    if local_ok and railway_ok:
        print("\n🎉 Both configurations are ready!")
        print("\n📝 Usage:")
        print("Local:   Use local.env for development")
        print("Railway: Use railway.env values in Railway dashboard")
        print("\n🚀 Next Steps:")
        print("1. Test local: Load local.env and run Odoo")
        print("2. Deploy to Railway: Set environment variables from railway.env")
    else:
        print("\n⚠️  Please fix the configuration issues above")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 