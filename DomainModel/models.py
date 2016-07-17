import uuid


class Itinerary:
    def __init__(self):
        self.Id = None
        self.Owner = None
        self.BookingDate = None
        self.Price = None
        self.Segments = []
        self.State = ItineraryState.Found


class ItinerarySegment:
    def __init__(self):
        self.Id = None
        self.Origin = None
        self.Destination = None
        self.DepartureTime = None
        self.ArrivalTime = None
        self.FlightStopsCount = None
        self.Duration = None
        self.FlightNumber = None


class ItinerarySearchRequest:
    def __init__(self, origin, destination, departure_date, return_date, round_trip):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date
        self.round_trip = round_trip


class ItinerarySearchResult(Itinerary):
    def __init__(self):
        self.search_id = str(uuid.uuid4())


class ItineraryState:
    Found = 1
    Booked = 2
    Paid = 3
