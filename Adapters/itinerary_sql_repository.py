import momoko
from tornado import gen
from tornado.ioloop import IOLoop


class ItinerarySqlRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    @gen.coroutine
    def init_db(self):
        # self.db = db

        ioloop = IOLoop.instance()

        self.db = momoko.Pool(
            dsn=self.connection_string,
            size=1,
            ioloop=ioloop,
        )

        # this is a one way to run ioloop in sync
        resultCon = yield self.db.connect()
        # ioloop.run_sync(lambda: future)
        # # ioloop.add_future(future, lambda f: ioloop.stop())
        # # ioloop.start()
        # future.result()  # raises exception on connection error

    @gen.coroutine
    def add(self, itinerary):
        # add itinerary
        cursor = yield self.db.execute(""" INSERT INTO public."Itinerary"(
                "Owner", "BookingDate", "Price", "State")
                VALUES (%s, %s, %s, %s)
                RETURNING "Id";""",
                                       (itinerary.Owner, itinerary.BookingDate, itinerary.Price, itinerary.State))

        itinerary.Id = cursor.fetchone()[0]

        # add itinerary segments
        segments = list(
            map(
                lambda x: (
                    x.Id,
                    itinerary.Id,
                    x.Origin,
                    x.Destination,
                    x.DepartureTime,
                    x.ArrivalTime,
                    x.FlightStopsCount,
                    x.Duration,
                    x.FlightNumber),
                itinerary.Segments))

        records_list_template = ','.join(['%s'] * len(segments))

        yield self.db.execute(""" INSERT INTO public."ItinerarySegment"(
                "Id", "ItineraryId", "Origin", "Destination", "DepartureTime",
                "ArrivalTime", "FlightStopsCount", "Duration", "FlightNumber")
                VALUES {0}""".format(records_list_template),
                              segments)

        return itinerary
