import Controllers.base_controller
from tornado import gen


class AirportsController(Controllers.base_controller.BaseHandler):
    def initialize(self, airports_repository):
        self.airports_repository = airports_repository

    @gen.coroutine
    def get(self, query):

        search_result = yield self.airports_repository.search(query)

        self.write(search_result)
