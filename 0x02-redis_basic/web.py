#!/usr/bin/env python3
""" this module is about Implementing an expiring web cache and tracker"""
from typing import Callable
import requests
import redis
count = 0


def get_page(url: str) -> str:
    """ get content of a page"""
    rc = redis.Redis()
    rc.set(f"cached:{url}", count)
    response = requests.get(url)
    rc.incr(f"count:{url}")
    rc.setex(f"cached:{url}", 10, rc.get(f"cached:{url}"))
    return response.text


if __name__ == "__main__":
    get_page('https://abidjan.net/')
