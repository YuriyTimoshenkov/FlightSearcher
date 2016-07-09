import DomainModel
from tornado import gen


class ItineraryService:
    def __init__(self, gds_service, itineraryRepository):
        self.gds_service = gds_service
        self.itineraryRepository = itineraryRepository
        self.itineraryRepository.init_db()

    def search(self, itinerary_search_request):
        return self.gds_service.search(itinerary_search_request)

    @gen.coroutine
    def book(self, itinerary):
        result = self.gds_service.book(itinerary)

        itinerary.State = DomainModel.models.ItineraryState.Booked
        itinerary = yield self.itineraryRepository.add(itinerary)

        return itinerary


