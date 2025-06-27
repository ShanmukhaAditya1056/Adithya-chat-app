from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

# Generate a random 32-byte AES key (use once or store securely)
def generate_key():
    return base64.urlsafe_b64encode(os.urandom(32)).decode()

# AES-256 CBC mode encryption
def encrypt_text(plain_text, key):
    key_bytes = base64.urlsafe_b64decode(key.encode())
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    result = base64.b64encode(iv + encrypted).decode()
    return result

def decrypt_text(encrypted_text, key):
    key_bytes = base64.urlsafe_b64decode(key.encode())
    data = base64.b64decode(encrypted_text)

    iv = data[:16]
    encrypted = data[16:]

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plain = unpadder.update(padded_plain) + unpadder.finalize()

    return plain.decode()

# Encrypt file (input path → output path)
def encrypt_file(input_path, output_path, key):
    with open(input_path, 'rb') as f:
        data = f.read()

    key_bytes = base64.urlsafe_b64decode(key.encode())
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_path, 'wb') as f:
        f.write(iv + encrypted)

# Decrypt file (input path → output path)
def decrypt_file(input_path, output_path, key):
    with open(input_path, 'rb') as f:
        data = f.read()

    key_bytes = base64.urlsafe_b64decode(key.encode())
    iv = data[:16]
    encrypted = data[16:]

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plain = unpadder.update(padded_plain) + unpadder.finalize()

    with open(output_path, 'wb') as f:
        f.write(plain)
