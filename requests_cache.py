from expiringdict import ExpiringDict
__cache = ExpiringDict(max_len=1000, max_age_seconds=600)


def cache_response(response, url):
    __cache[url] = response


def get_cached_response(url):
    response = __cache.get(url)
    return response
