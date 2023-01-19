#!/usr/bin/env python3
""" this module is about Implementing an expiring web cache and tracker"""
import requests
import redis
rc = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """ get content of a page"""
    rc.set(f"cached:{url}", count)
    response = requests.get(url)
    rc.incr(f"count:{url}")
    rc.setex(f"cached:{url}", 10, rc.get(f"cached:{url}"))
    return response.text


if __name__ == "__main__":
    get_page('https://abidjan.net/')
