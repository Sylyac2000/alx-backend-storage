#!/usr/bin/env python3
""" this module is about Implementing an expiring web cache and tracker"""

import requests
import redis
import functools


def cache_and_count(func):
    """cache the output"""
    @functools.wraps(func)
    def wrapper(url: str):
        r = redis.Redis()
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"
        if r.exists(cache_key):
            r.incr(count_key)
            return r.get(cache_key).decode()

        result = func(url)
        r.set(cache_key, result, ex=10)
        r.incr(count_key)
        return result
    return wrapper


@cache_and_count
def get_page(url: str) -> str:
    """ get content of a page"""
    response = requests.get(url)
    html = response.text
    return html
