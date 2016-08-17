import json

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado import gen


class AirportsRepository:
    def __init__(self, access_key, source_url):
        self.access_key = access_key
        self.source_url = source_url

    @gen.coroutine
    def search(self, query):
        http_client = AsyncHTTPClient()

        url = self.source_url + ('?api_key={}&query={}'.format(
            self.access_key,
            query))

        response = yield http_client.fetch(HTTPRequest(url))

        serilizedResult = response.body.decode("utf-8")

        result = json.loads(serilizedResult)

        return result["response"]