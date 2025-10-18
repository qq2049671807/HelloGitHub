import os
from cryptography.fernet import Fernet


class CryptoManager:
    def __init__(self, key_file='secret.key'):
        self.key_file = key_file
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt(self, text):
        if not text:
            return ''
        return self.cipher.encrypt(text.encode()).decode()
    
    def decrypt(self, encrypted_text):
        if not encrypted_text:
            return ''
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            return f"解密失败: {str(e)}"
