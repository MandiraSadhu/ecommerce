import os
import base64
from cryptography.fernet import Fernet

# Retrieve the key from environment variables
KEY = os.environ.get('ENCRYPTION_KEY').encode('utf-8')
cipher_suite = Fernet(KEY)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt_data(data):
    try:
        # Add padding before decoding
        padded_data = data + '=='
        decoded_data = base64.urlsafe_b64decode(padded_data.encode('utf-8'))
        return cipher_suite.decrypt(decoded_data).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")
