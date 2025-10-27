from data_setup.ingestion_interfaces import Encryption


class BasicEncryption(Encryption):
    """
    A simple demonstration encryption system using character shifting (Caesar cipher style).
    Each permission level has its own numeric shift key.
    """

    def __init__(self):
        # Define simple numeric keys for each permission level
        self.keys: Dict[str, int] = {
            "public": 3,     # shift by 3
            "employee": 8,   # shift by 8
            "admin": 13      # shift by 13
        }

    def encrypt(self, plaintext: str, permission_level: str) -> str:
        """
        Encrypt text by shifting each character's ASCII code based on permission level.
        Not secure — for demonstration only.
        """
        key = self.keys.get(permission_level)
        if key is None:
            raise ValueError(f"Invalid permission level: {permission_level}")

        ciphertext = ""
        for char in plaintext:
            # Only shift letters; leave others unchanged
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                ciphertext += chr((ord(char) - base + key) % 26 + base)
            else:
                ciphertext += char

        return ciphertext

    
    def decrypt(self, ciphertext: str, permission_level: str) -> str:
        """
        Decrypt text by reversing the character shift based on permission level.
        """
        key = self.keys.get(permission_level)
        if key is None:
            raise ValueError(f"Invalid permission level: {permission_level}")

        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                plaintext += chr((ord(char) - base - key) % 26 + base)
            else:
                plaintext += char

        return plaintext





