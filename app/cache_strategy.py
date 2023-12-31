from flask import Request
from flask_caching import Cache

from app.models import Technology

TECHNOLOGY = 'technology'
TIMEOUT = 81600


def make_cache_key(page: str, args_dict: dict, **kwargs):
    key = [page]
    for key, value in args_dict.values():
        key.append(f'{key}={value}')
    return ''.join(key)


def cache_technology(cache: Cache):
    if cached_technology := cache.get(TECHNOLOGY):
        return cached_technology
    with cache.app.app_context():
        languages = [i.title for i in Technology.query.all()]
        cache.set(TECHNOLOGY, languages, timeout=TIMEOUT)
        return languages


def cache_page(cache: Cache, request: Request, template_render, *args, **kwargs):
    key = make_cache_key('main', request.args)
    if cached_page := cache.get(key):
        return cached_page
    with cache.app.app_context():
        template = template_render(args, kwargs)
        cache.set(key, template, timeout=TIMEOUT)
        return template
