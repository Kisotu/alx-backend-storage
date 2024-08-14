#!/usr/bin/env python3
"""A module for caching and tracking HTTP requests.
"""
import redis
import requests
from typing import Callable
from functools import wraps


redis_store = redis.Redis()
"""the Redis instance to store cached data
"""


def data_cacher(method: Callable) -> Callable:
    """
    Caches the response of an HTTP request.
    Args:
        method: A function that makes an HTTP request.
    Returns:
        A wrapper function that caches the response.
    """
    @wraps(method)
    def invoke(url) -> str:
        """
        Makes an HTTP request and caches the response.
        Args:
            url: The URL to request.
        Returns:
            The response of the HTTP request.
        """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoke


@data_cacher
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response.
    Args:
        url: The URL to request.
    Returns:
        The content of the requested URL.
    """
    return requests.get(url).text
