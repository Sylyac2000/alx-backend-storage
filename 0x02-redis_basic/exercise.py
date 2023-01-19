#!/usr/bin/env python3
""" this module is about Cache class"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def replay(method: Callable) -> None:
    """displays the history of calls of a particular function"""
    method_key = method.__qualname__
    inputs = method_key + ':inputs'
    outputs = method_key + ':outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, out in list(IOTuple):
        attr, data = inp.decode("utf-8"), out.decode("utf-8")
        print(f'{method_key}(*{attr}) -> {data}')


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    method_key = method.__qualname__
    inputs = method_key + ':inputs'
    outputs = method_key + ':outputs'

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        resultat = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(resultat))
        return resultat
    return wrapped


def count_calls(method: Callable) -> Callable:
    """ count number of call"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
