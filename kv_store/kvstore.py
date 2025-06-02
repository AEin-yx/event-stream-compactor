import time
import json
import os,sys
from pathlib import Path

class InMemoryKV:
    """
        Create a file called kvstore.json and update it to reflect the state of the current memory
        functions present: get(key), set(key,value), delete(key), print()
    """
    def __init__(self,storage_file="kvstore.json"):
        self.storage_file = storage_file
        self.cache={}
        self.ttl={}
        self.load_from_disk()

    def load_from_disk(self):
        """Load data from disk on startup"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.cache = data.get('cache', {})
                    self.ttl = data.get('ttl', {})
                    # Clean up expired keys on load
                    self._cleanup_expired_on_load()
            except (json.JSONDecodeError, FileNotFoundError):
                self.cache = {}
                self.ttl = {}

    def save_to_disk(self):
        """Save current state to disk"""
        data = {
            'cache': self.cache,
            'ttl': self.ttl
        }
    
        # Cross-platform atomic write
        temp_file = self.storage_file + '.tmp'
        try:
            # Write to temp file
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)
        
            # Atomic replace (works on Windows + Unix)
            if os.name == 'nt':  # Windows
                if os.path.exists(self.storage_file):
                    os.remove(self.storage_file)
                os.rename(temp_file, self.storage_file)
            else:  # Unix/Linux/Mac
                os.rename(temp_file, self.storage_file)
            
        except Exception as e:
            # Cleanup temp file if something goes wrong
            if os.path.exists(temp_file):
                os.remove(temp_file)
            print(f"Warning: Failed to save data - {e}")
            # Fallback: direct write (not atomic but works)
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
    
    def _cleanup_expired_on_load(self):
        """Remove expired keys when loading from disk"""
        current_time = time.time()
        expired_keys = [
            key for key, expiry in self.ttl.items()
            if expiry <= current_time
        ]
        for key in expired_keys:
            self.delete_key(key, save=False)  # Don't save during load
    
    # write-through cache pattern ->immediate persistence for consistency and simplicity during development
    # For production scale, I'd add batching and async writes

    def set_key_value(self,key: str, value: str, ttl: int = None):
        self.cache[key]=value
        if ttl:
            self.ttl[key]=time.time()+ttl
        elif key in self.ttl:
            del self.ttl[key]  # Remove TTL if not specified
        self.save_to_disk()  # Persist after each write

    def get_value(self,key:str): 

        # lazy cleanup 
        # Check TTL expiration
        if key in self.ttl and time.time() > self.ttl[key]:
            self.delete_key(key)
            return None
        
        self.save_to_disk()
        
        # Check key in cache? (Yes or No)
        if key not in self.cache:
            return None
    
        found_value = self.cache[key]
        return found_value

    def delete_key(self,key:str,save=True):
        if key in self.cache:
            del self.cache[key]
        if key in self.ttl:
            del self.ttl[key]
        if save:
            self.save_to_disk()


    # test to check if kvstore.json reflect the cache and ttl of this class
    def printall(self):
        for key,value in self.cache.items():
            print(f'cache {key}:{value}')
        
        for key,value in self.ttl.items():
            print(f" ttl  {key}:{value}")
