#!/usr/bin/env python3
import sys
sys.path.append('/app')  # Add container working directory to path
import os, sys, time, datetime
import base64

# Make sure /app is in path to import totp_generator
sys.path.append("/app")
from totp_generator import generate_totp_code

SEED_FILE = "/data/seed.txt"

try:
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()
    code = generate_totp_code(hex_seed)
except Exception as e:
    code = f"Error: {e}"

# Get UTC timestamp
timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Print output
print(f"{timestamp} - 2FA Code: {code}")
