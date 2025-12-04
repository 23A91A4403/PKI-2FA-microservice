# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from totp_generator import generate_totp_code, verify_totp_code
import time

app = FastAPI()

DATA_FILE = "data/seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"

# Make sure 'data' folder exists
os.makedirs("data", exist_ok=True)

class EncryptedSeed(BaseModel):
    encrypted_seed: str

class CodeModel(BaseModel):
    code: str

# Endpoint 1: Decrypt seed
@app.post("/decrypt-seed")
def decrypt_seed_api(data: EncryptedSeed):
    try:
        with open(PRIVATE_KEY_FILE, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)
        
        encrypted_bytes = base64.b64decode(data.encrypted_seed)

        decrypted = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        hex_seed = decrypted.decode().strip()

        if len(hex_seed) != 64 or not all(c in "0123456789abcdef" for c in hex_seed):
            raise ValueError("Invalid seed format")

        with open(DATA_FILE, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}
    except:
        raise HTTPException(status_code=500, detail={"error": "Decryption failed"})

# Endpoint 2: Generate TOTP
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    
    with open(DATA_FILE, "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    remaining = 30 - (int(time.time()) % 30)
    return {"code": code, "valid_for": remaining}

# Endpoint 3: Verify TOTP
@app.post("/verify-2fa")
def verify_2fa(data: CodeModel):
    if not data.code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    with open(DATA_FILE, "r") as f:
        hex_seed = f.read().strip()

    is_valid = verify_totp_code(hex_seed, data.code)
    return {"valid": is_valid}
