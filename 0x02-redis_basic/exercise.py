#!/usr/bin/env python3
""" this module is about Cache class"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


class Cache:

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(fn: Callable) -> Callable:
        """ count number of call"""
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            self._redis.incr(fn.__qualname__)
            return fn(self, *args, **kwargs)
        return wrapped

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """return a generate a random key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> str:
        """ return element """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ return a string"""
        return key.decode('utf-8', 'strict')

    def get_int(self, key: str) -> int:
        """ return a int"""
        return int(key)
