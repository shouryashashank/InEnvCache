import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time
import base64
import os
import threading
from kubernetes import client, config

class InEnvCache:
    def __init__(self, key=None, configmap_name="iec-configmap", namespace="default"):
        self.cache = {}
        self.enableEncryption = False
        self.lock = threading.Lock()
        if key is not None and isinstance(key, str):
            self.enableEncryption = True
            self.key = key.encode()
        # Check if the Kubernetes API is available
        try: 
            self.v1.get_api_resources()
            # Kubernetes API is available
            # Load the kubeconfig file
            config.load_kube_config()

            # Create a client for the Core V1 API
            self.v1 = client.CoreV1Api()

            # Set the ConfigMap name and namespace
            self.configmap_name = configmap_name
            self.namespace = namespace
            self.kubernetes_cache = True
            pass
        except Exception as e:
            print(e)
            # Kubernetes API is not available
            self.kubernetes_cache = False

    def _pad_key(self, key):
        # Pad the key to be 16, 24, or 32 bytes long
        while len(key) not in [16, 24, 32]:
            key += b'\0'  # Padding with null bytes
        return key
    
    def _encrypt(self, data):
        padded_key = self._pad_key(self.key)
        cipher = AES.new(padded_key, AES.MODE_EAX)
        nonce = cipher.nonce
        cipher_text, tag = cipher.encrypt_and_digest(data.encode())
        return [base64.b64encode(x).decode('utf-8') for x in (nonce, cipher_text, tag)]

    def _decrypt(self, enc_data):
        padded_key = self._pad_key(self.key)
        nonce, cipher_text, tag = [base64.b64decode(x.encode('utf-8')) for x in enc_data]
        cipher = AES.new(padded_key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(cipher_text, tag).decode()

    def set(self, key, value, ttl=None):
        with self.lock:
            key = "InEnvCache_"+str(key)
            if self.enableEncryption:
                value = self._encrypt(value)
            cache_value = {'value': value, 'expiry': time.time() + ttl if ttl else None}
            if self.kubernetes_cache:
                # Read the ConfigMap
                config_map = self.v1.read_namespaced_config_map(name=self.configmap_name, namespace=self.namespace)

                # Update the ConfigMap
                if config_map.data is None:
                    config_map.data = {}
                config_map.data[key] = json.dumps(cache_value)
                self.v1.patch_namespaced_config_map(name=self.configmap_name, namespace=self.namespace, body=config_map)
            else:
                os.environ[key] = json.dumps(cache_value)
            

    def get(self, key):
        with self.lock:
            cache_value = None
            cache_key = "InEnvCache_"+str(key)
            if self.kubernetes_cache:
                # Read the ConfigMap
                config_map = self.v1.read_namespaced_config_map(name=self.configmap_name, namespace=self.namespace)

                # Get the value from the ConfigMap
                cache_value = config_map.data.get(cache_key)
            else:
                cache_value = os.getenv(cache_key)
            if cache_value is None:
                return None
            cache_value = json.loads(cache_value)
            if cache_value is None or (cache_value['expiry'] is not None and time.time() > cache_value['expiry']):
                return None
            value = cache_value['value']
            if self.enableEncryption:
                value = self._decrypt(value)
            return value

    def delete(self, key):
        with self.lock:
            key = "InEnvCache_"+str(key)

            if self.kubernetes_cache:
                # Read the ConfigMap
                config_map = self.v1.read_namespaced_config_map(name=self.configmap_name, namespace=self.namespace)

                # Update the ConfigMap
                if config_map.data is not None:
                    del config_map.data["InEnvCache_"+str(key)]
                    self.v1.patch_namespaced_config_map(name=self.configmap_name, namespace=self.namespace, body=config_map)
            else:
                if key in os.environ:
                    del os.environ[key]


    def flush_all(self):
        with self.lock:
            if self.kubernetes_cache:
                # Read the ConfigMap
                config_map = self.v1.read_namespaced_config_map(name=self.configmap_name, namespace=self.namespace)

                # Update the ConfigMap
                if config_map.data is not None:
                    keys_to_delete = [key for key in config_map.data if key.startswith("InEnvCache_")]
                    for key in keys_to_delete:
                        del config_map.data[key]
                    self.v1.patch_namespaced_config_map(name=self.configmap_name, namespace=self.namespace, body=config_map)
            else:
                keys_to_delete = [key for key in os.environ if key.startswith("InEnvCache_")]
                for key in keys_to_delete:
                    del os.environ[key]

# if __name__ == "__main__":
#     # Create an instance of InEnvCache
#     cache = InEnvCache(key="my-secret-key", configmap_name="my-configmap", namespace="default")

#     # Set a value in the cache
#     cache.set("key1", "value1", ttl=600)

#     # Get a value from the cache
#     value = cache.get("key1")
#     print(value)  # Output: value1

#     # Delete a value from the cache
#     cache.delete("key1")

#     # Flush all values from the cache
#     cache.flush_all()