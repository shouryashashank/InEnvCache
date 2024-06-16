import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time
import base64
import os
import threading

class InEnvCache:
    def __init__(self, key=None):
        self.cache = {}
        self.enableEncryption = False
        self.lock = threading.Lock()
        if key is not None and isinstance(key, str):
            self.enableEncryption = True
            self.key = key.encode()

    def _encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        cipher_text, tag = cipher.encrypt_and_digest(data.encode())
        return [base64.b64encode(x).decode('utf-8') for x in (nonce, cipher_text, tag)]

    def _decrypt(self, enc_data):
        nonce, cipher_text, tag = [base64.b64decode(x.encode('utf-8')) for x in enc_data]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(cipher_text, tag).decode()

    def set(self, key, value, ttl=None):
        with self.lock:
            key = "InEnvCache_"+str(key)
            if self.enableEncryption:
                value = self.encrypt(value)
            cache_value = {'value': value, 'expiry': time.time() + ttl if ttl else None}
            os.environ[key] = json.dumps(cache_value)

    def get(self, key):
        with self.lock:
            cache_key = "InEnvCache_"+str(key)
            entry = os.getenv(cache_key)
            if entry is None:
                return None
            entry = json.loads(entry)
            if entry is None or (entry['expiry'] is not None and time.time() > entry['expiry']):
                self.delete(key)
                return None
            value = entry['value']
            if self.enableEncryption:
                value = self.decrypt(value)
            return value

    def delete(self, key):
        with self.lock:
            key = "InEnvCache_"+str(key)
            if key in os.environ:
                del os.environ[key]

    def flush_all(self):
        with self.lock:
            keys_to_delete = [key for key in os.environ if key.startswith("InEnvCache_")]
            for key in keys_to_delete:
                del os.environ[key]