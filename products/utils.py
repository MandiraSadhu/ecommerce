from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt_data(data):
    return cipher_suite.decrypt(data.encode('utf-8')).decode('utf-8')
