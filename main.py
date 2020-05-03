from urllib.parse import urlparse
from aiohttp import web
import aiohttp
import requests_cache
import ip_buffers_collection

BASE_URL = 'https://reqres.in/api'


def filter_ip(ip):
    is_valid = ip_buffers_collection.check_ip(ip)
    if is_valid:
        ip_buffers_collection.add_ip(ip)
    return is_valid


def response_from_tuple(res_tuple):
    return web.Response(text=res_tuple[0], content_type=res_tuple[1])


async def handle(request):
    controller = request.match_info.get('controller', "default")
    if controller == "users":
        if not filter_ip(request.remote):
            return web.Response(text='too many requests, too little time')
        if request.method == "GET":
            cached_tuple = requests_cache.get_cached_response(request.rel_url)
            if cached_tuple is not None:
                return response_from_tuple(cached_tuple)

        async with aiohttp.ClientSession() as session:
            url = BASE_URL + str(request.rel_url)
            proxy_response = await session.request(request.method, url)
            res_text = await proxy_response.text()
            res_cache_tuple = (res_text, proxy_response.content_type)
            response = response_from_tuple(res_cache_tuple)
            if response.status < 300:
                requests_cache.cache_response(res_cache_tuple, request.rel_url)
            return response
    else:
        return web.Response(text="failed")


app = web.Application()
app.add_routes([web.get('/{controller}/{tail:.*}', handle),
                web.get('/{controller}', handle),
                web.get('/', handle),
                web.post('/{controller}/{tail:.*}', handle),
                web.post('/{controller}', handle),
                web.post('/', handle),
                web.delete('/{controller}/{tail:.*}', handle),
                web.delete('/{controller}', handle),
                web.delete('/', handle),
                web.put('/{controller}/{tail:.*}', handle),
                web.put('/{controller}', handle),
                web.put('/', handle),
                web.patch('/{controller}/{tail:.*}', handle),
                web.patch('/{controller}', handle),
                web.patch('/', handle),
                web.head('/{controller}/{tail:.*}', handle),
                web.head('/{controller}', handle),
                web.head('/', handle)
                ])

if __name__ == '__main__':
    web.run_app(app)
