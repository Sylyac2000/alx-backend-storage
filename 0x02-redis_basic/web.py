#!/usr/bin/env python3
""" this module is about Implementing an expiring web cache and tracker"""
import requests
import redis
rc = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """ get content of a page"""
    r = redis.Redis()
    count_key = f"count:{url}"
    cache_key = f"cache:{url}"

    if r.exists(cache_key):
        r.incr(count_key)
        return r.get(cache_key).decode()

    response = requests.get(url)
    html = response.text
    r.set(cache_key, html, ex=10)
    r.incr(count_key)
    return html


if __name__ == "__main__":
    get_page('https://abidjan.net/')
