import os
import sys
import json
import pytest

# Add project root to sys.path
sys.path.append(os.path.abspath(os.getcwd()))
from data_setup.encryption_system.aes_encryption import AESEncryption
import base64, os
print(base64.b64encode(os.urandom(32)).decode())
print(base64.b64encode(os.urandom(32)).decode())
print(base64.b64encode(os.urandom(32)).decode())