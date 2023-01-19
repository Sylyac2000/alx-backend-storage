#!/usr/bin/env python3
"""
this module is about Implementing an expiring web cache and tracker
"""
from typing import Callable
from functools import wraps
import redis
import requests
redis_store = redis.Redis()


def cache_and_count(method: Callable) -> Callable:
    """counts how many times an url is called"""
    @wraps(method)
    def wrapper(url) -> str:
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_and_count
def get_page(url: str) -> str:
    """get a page and cache value"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('https://abidjan.net/')
