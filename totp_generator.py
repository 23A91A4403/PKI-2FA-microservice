import base64
import pyotp

def generate_totp_code(hex_seed: str) -> str:
    # 1. Convert hex → bytes
    seed_bytes = bytes.fromhex(hex_seed)

    # 2. Convert bytes → base32
    base32_seed = base64.b32encode(seed_bytes).decode()

    # 3. Create TOTP object (SHA1, 30 sec, 6 digits — DEFAULT)
    totp = pyotp.TOTP(base32_seed)

    # 4. Generate current TOTP
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    # Same conversion
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)

    # Verify with ±30 seconds window
    return totp.verify(code, valid_window=valid_window)


if __name__ == "__main__":
    hex_seed = input("Enter your 64-character hex seed: ")

    code = generate_totp_code(hex_seed)
    print("Your TOTP code:", code)

    verify = verify_totp_code(hex_seed, code)
    print("Is the code valid?", verify)
