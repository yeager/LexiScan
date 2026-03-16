"""Simple on-disk cache for API responses."""

import hashlib
import json
import os
import time


class DiskCache:
    """LRU-style disk cache for API responses and images."""

    def __init__(self, cache_dir=None, max_size_mb=50):
        if cache_dir is None:
            cache_dir = os.path.join(
                os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")),
                "lexiscan",
            )
        self._cache_dir = cache_dir
        self._max_size = max_size_mb * 1024 * 1024
        os.makedirs(self._cache_dir, exist_ok=True)

    def _key_to_path(self, key: str) -> str:
        h = hashlib.sha256(key.encode()).hexdigest()[:16]
        return os.path.join(self._cache_dir, h)

    def get(self, key: str, max_age_seconds: int = 86400):
        """Get cached value. Returns None if not found or expired."""
        path = self._key_to_path(key)
        if not os.path.exists(path):
            return None

        age = time.time() - os.path.getmtime(path)
        if age > max_age_seconds:
            os.unlink(path)
            return None

        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def put(self, key: str, value):
        """Store a value in the cache."""
        path = self._key_to_path(key)
        try:
            with open(path, "w") as f:
                json.dump(value, f)
        except (IOError, TypeError):
            pass

    def get_bytes(self, key: str, max_age_seconds: int = 86400):
        """Get cached binary data."""
        path = self._key_to_path(key) + ".bin"
        if not os.path.exists(path):
            return None

        age = time.time() - os.path.getmtime(path)
        if age > max_age_seconds:
            os.unlink(path)
            return None

        try:
            with open(path, "rb") as f:
                return f.read()
        except IOError:
            return None

    def put_bytes(self, key: str, data: bytes):
        """Store binary data in the cache."""
        path = self._key_to_path(key) + ".bin"
        try:
            with open(path, "wb") as f:
                f.write(data)
        except IOError:
            pass
