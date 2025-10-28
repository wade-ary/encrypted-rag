from data_setup.ingestion_interfaces import Encryption
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
from dotenv import load_dotenv
class AESEncryption(Encryption):



    def __init__(self):
        """
        Initialize AES-GCM keys for each permission level.
        Each key is 32 bytes (256-bit) for strong encryption.
        """
        load_dotenv()
        self.keys = {
            "public": AESGCM(base64.b64decode(os.getenv("PUBLIC_KEY"))),
            "employee": AESGCM(base64.b64decode(os.getenv("EMPLOYEE_KEY"))),
            "admin": AESGCM(base64.b64decode(os.getenv("ADMIN_KEY")))
        }

    def encrypt(self, plaintext: str, permission_level: str) -> str:
        """
        Encrypt plaintext using AES-GCM for the given permission level.
        Returns base64-encoded ciphertext (nonce + encrypted data).
        """
        aesgcm = self.keys.get(permission_level)
        if aesgcm is None:
            raise ValueError(f"Invalid permission level: {permission_level}")

        # Generate a 12-byte random nonce (recommended for AES-GCM)
        nonce = os.urandom(12)

        # Encrypt (associated_data = None for simplicity)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

        # Combine nonce + ciphertext, then base64 encode for storage
        encrypted_blob = base64.b64encode(nonce + ciphertext).decode()

        return encrypted_blob

    def decrypt(self, ciphertext: str, permission_level: str) -> str:
        """
        Decrypt base64-encoded ciphertext (nonce + encrypted data)
        using AES-GCM for the given permission level.
        """
        aesgcm = self.keys.get(permission_level)
        if aesgcm is None:
            raise ValueError(f"Invalid permission level: {permission_level}")

        # Decode from base64 to raw bytes
        data = base64.b64decode(ciphertext.encode())

        # The first 12 bytes are the nonce, the rest is the ciphertext
        nonce, encrypted_data = data[:12], data[12:]

        # Decrypt (associated_data = None for simplicity)
        plaintext = aesgcm.decrypt(nonce, encrypted_data, None)

        return plaintext.decode()
    