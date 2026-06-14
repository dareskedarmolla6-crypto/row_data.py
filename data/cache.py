import time
import threading


class CacheItem:
    def __init__(self, value, ttl):
        self.value = value
        self.expiry = time.time() + ttl


class CacheManager:
    """
    High-speed in-memory cache for market data, signals, and computed features.
    Used across:
    - brain
    - strategy
    - execution
    - alpha scanner
    """

    def __init__(self, default_ttl=5):
        self.store = {}
        self.default_ttl = default_ttl
        self.lock = threading.Lock()

    # =========================
    # SET CACHE
    # =========================
    def set(self, key, value, ttl=None):
        ttl = ttl or self.default_ttl

        with self.lock:
            self.store[key] = CacheItem(value, ttl)

    # =========================
    # GET CACHE
    # =========================
    def get(self, key, default=None):
        with self.lock:
            item = self.store.get(key)

            if not item:
                return default

            # expired
            if time.time() > item.expiry:
                del self.store[key]
                return default

            return item.value

    # =========================
    # CHECK EXISTENCE
    # =========================
    def exists(self, key):
        return self.get(key, None) is not None

    # =========================
    # DELETE KEY
    # =========================
    def delete(self, key):
        with self.lock:
            if key in self.store:
                del self.store[key]

    # =========================
    # CLEAR ALL CACHE
    # =========================
    def clear(self):
        with self.lock:
            self.store.clear()

    # =========================
    # CLEANUP EXPIRED KEYS
    # =========================
    def cleanup(self):
        with self.lock:
            now = time.time()
            keys_to_delete = [
                k for k, v in self.store.items()
                if now > v.expiry
            ]
            for k in keys_to_delete:
                del self.store[k]

    # =========================
    # BULK OPERATIONS (optional FSE use)
    # =========================
    def set_many(self, data_dict, ttl=None):
        for k, v in data_dict.items():
            self.set(k, v, ttl)

    def get_many(self, keys):
        return {k: self.get(k) for k in keys}
# Safety improvement: prevent dead cache reads (race-safe cleanup helper)
def safe_get(self, key, default=None):
    try:
        return self.get(key, default)
    except Exception:
        return default
