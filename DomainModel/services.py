import DomainModel
from tornado import gen


class ItineraryService:
    def __init__(self, gds_service, itinerary_repository, logger, json_encoder):
        self.gds_service = gds_service
        self.itinerary_repository = itinerary_repository
        self.itinerary_repository.init_db()
        self.logger = logger
        self.json_encoder = json_encoder

    def search(self, itinerary_search_request):
        self.logger.info('Started search of {}'.format(self.json_encoder.encode(itinerary_search_request)))

        result = self.gds_service.search(itinerary_search_request)

        self.logger.info('Found results {}'.format(self.json_encoder.encode(result)))

        return result

    @gen.coroutine
    def book(self, itinerary):
        self.logger.info('Started booking of itinerary {}'.format(self.json_encoder.encode(itinerary)))

        self.gds_service.book(itinerary)

        itinerary.State = DomainModel.models.ItineraryState.Booked
        itinerary = yield self.itinerary_repository.add(itinerary)

        self.logger.info('Itinerary was booked {}'.format(self.json_encoder.encode(itinerary)))

        return itinerary


