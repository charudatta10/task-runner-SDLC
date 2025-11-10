# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import hashlib
from cryptography.fernet import Fernet

def get_hash(text):
    """Get the hash of a string"""
    return hashlib.sha256(text.encode()).hexdigest()

def encrypt_text(text, key):
    """Encrypt text"""
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt_text(token, key):
    """Decrypt text"""
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

def generate_key():
    """Generate a key for encryption"""
    return Fernet.generate_key().decode()
