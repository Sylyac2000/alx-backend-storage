#!/usr/bin/env python3
""" this module is about Cache class"""
import redis
import uuid
from typing import Union


class Cache:

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """return a generate a random key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
