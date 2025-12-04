import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

def load_private_key(path):
    with open(path, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
    return key

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    # Step 1: Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    # Step 2: RSA Decrypt with OAEP + SHA256
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Step 3: Convert bytes → UTF-8 string
    seed_hex = decrypted_bytes.decode("utf-8")

    # Step 4: Validation
    if len(seed_hex) != 64:
        raise ValueError("Seed must be 64 characters")
    if not all(c in "0123456789abcdef" for c in seed_hex):
        raise ValueError("Seed must be valid hexadecimal")

    return seed_hex


# ------------ TEST (you will replace later) -------------

if __name__ == "__main__":
    private_key = load_private_key("student_private.pem")
    encrypted_input = input("Enter encrypted seed (Base64): ")

    seed = decrypt_seed(encrypted_input, private_key)
    print("\nDecrypted seed:")
    print(seed)
