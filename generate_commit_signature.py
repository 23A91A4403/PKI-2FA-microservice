import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

# ===== CONFIG =====
commit_hash = "cb08e0bfc9985422b8308b7c6c6b2387fd8dc1d6"
private_key_file = "student_private.pem"
instructor_pub_file = "instructor_public.pem"

# ===== LOAD STUDENT PRIVATE KEY =====
with open(private_key_file, "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# ===== SIGN COMMIT HASH =====
# RSA-PSS with SHA-256, max salt length
signature = private_key.sign(
    commit_hash.encode("utf-8"),  # Sign ASCII bytes of commit hash
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# ===== LOAD INSTRUCTOR PUBLIC KEY =====
with open(instructor_pub_file, "rb") as f:
    instructor_public = serialization.load_pem_public_key(f.read())

# ===== ENCRYPT SIGNATURE =====
encrypted_signature = instructor_public.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# ===== BASE64 ENCODE =====
b64_signature = base64.b64encode(encrypted_signature).decode("utf-8")

print("Commit Hash:", commit_hash)
print("Encrypted Commit Signature (single line):")
print(b64_signature)
