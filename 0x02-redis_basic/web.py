#!/usr/bin/env python3
""" this module is about Implementing an expiring web cache and tracker"""
from typing import Callable
import requests
import redis
import functools


def cache_and_count(method: Callable) -> Callable:
    """count how many times """
    @functools.wraps(method)
    def wrapper(url) -> str:
        r = redis.Redis()
        r.incr(f"count:{url}")
        result = r.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        r.set(f'count:{url}', 0)
        r.setex(f'result:{url}', 10, result)
    return wrapper


@cache_and_count
def get_page(url: str) -> str:
    """ get content of a page"""
    response = requests.get(url)
    html = response.text
    return html
