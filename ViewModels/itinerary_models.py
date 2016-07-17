import tornado
import Common
import DomainModel.models
import utils.json_datetime_encoder
import json
import  sys


class ItinerarySearchViewModel:
    def __init__(self, request_arguments):
        try:
            self.origin = request_arguments['origin']
            self.destination = request_arguments['destination']
            self.departure_date = request_arguments['departure_date']
            self.return_date = request_arguments['return_date']
            self.round_trip = request_arguments['round_trip']
        except:
            raise Common.exceptions.ValidationModelException('ItinerarySearchViewModel validation error. Details: {}'
                                                             .format(sys.exc_info()[0]))

    def to_domain_model(self):
        result = DomainModel.models.ItinerarySearchRequest(
            self.origin,
            self.destination,
            self.departure_date,
            self.return_date,
            self.round_trip)

        return result


class ItineraryBookViewModel:
    def __init__(self, json_model):
        self.__dict__ = json.loads(json_model)

    def to_domain_model(self):
        result = DomainModel.models.Itinerary()

        result.__dict__ = self.__dict__
        result.Segments = list(map(ItineraryBookViewModel.segment_to_domain_model, self.Segments))

        return result

    @staticmethod
    def segment_to_domain_model(segment_dict):
        result = DomainModel.models.ItinerarySegment()
        result.__dict__ = segment_dict

        return result

