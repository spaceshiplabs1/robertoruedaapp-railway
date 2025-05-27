#!/usr/bin/env python3
"""
Environment Configuration for Roberto Rueda Fitness App
Automatically detects local vs Railway environment and loads appropriate settings
"""

import os
import sys
from pathlib import Path

def detect_environment():
    """
    Detect if we're running locally or on Railway
    Returns: 'local' or 'railway'
    """
    # Railway sets specific environment variables
    if os.getenv('RAILWAY_ENVIRONMENT'):
        return 'railway'
    
    # Check for Railway-specific paths
    if os.path.exists('/mnt/extra-addons') or os.getenv('PORT') and not os.path.exists('/Users'):
        return 'railway'
    
    # Default to local if we can't detect Railway
    return 'local'

def load_environment_config():
    """
    Load the appropriate environment configuration
    """
    env = detect_environment()
    
    if env == 'local':
        env_file = 'local.env'
        print("🏠 Detected LOCAL environment")
    else:
        env_file = 'railway.env'
        print("🚀 Detected RAILWAY environment")
    
    # Load environment variables from the appropriate file
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        print(f"✅ Loaded configuration from {env_file}")
    else:
        print(f"⚠️  Warning: {env_file} not found")
    
    return env

def get_config():
    """
    Get configuration values based on current environment
    """
    env = load_environment_config()
    
    config = {
        'environment': env,
        'db_host': os.getenv('DB_HOST', 'localhost'),
        'db_port': os.getenv('DB_PORT', '5432'),
        'db_user': os.getenv('DB_USER', 'spaceshiplabs'),
        'db_password': os.getenv('DB_PASSWORD', 'admin'),
        'db_name': os.getenv('DB_NAME', 'test_odoo'),
        'port': os.getenv('PORT', '8069'),
        'workers': os.getenv('WORKERS', '0' if env == 'local' else '2'),
        'addons_path': os.getenv('ADDONS_PATH', ''),
        'data_dir': os.getenv('DATA_DIR', ''),
        'admin_password': os.getenv('ADMIN_PASSWORD', 'admin'),
        'list_db': os.getenv('LIST_DB', 'True' if env == 'local' else 'False'),
        'enterprise_code': os.getenv('ENTERPRISE_CODE', 'M250509223391128'),
    }
    
    return config

if __name__ == '__main__':
    config = get_config()
    print("\n📋 Current Configuration:")
    for key, value in config.items():
        if 'password' in key.lower():
            print(f"  {key}: {'*' * len(str(value))}")
        else:
            print(f"  {key}: {value}") 