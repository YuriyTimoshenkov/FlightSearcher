import tornado
import tornado.httpclient
import tornado.template
import Common.authdecorator
import Controllers.baseController
import ViewModels.itinerary_models
import utils.json_datetime_encoder
from Common.exceptions import  ValidationModelException
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import DomainModel.services


class ItineraryController(Controllers.baseController.BaseHandler):
    @gen.coroutine
    def initialize(self, itinerary_service, json_encoder, auth_key):
        self.itinerary_service = itinerary_service
        self.json_encoder = json_encoder
        self.rsa_key_string = auth_key

    @gen.coroutine
    def get(self):
        arguments = {k: self.get_argument(k) for k in self.request.arguments}

        view_model = ViewModels.itinerary_models.ItinerarySearchViewModel(arguments)
        domain_model = view_model.to_domain_model()

        result = self.itinerary_service.search(domain_model)

        self.write(self.json_encoder.encode(result))

    @Common.authdecorator.authenticate
    @gen.coroutine
    def post(self):
        booking_model = ViewModels.itinerary_models.ItineraryBookViewModel(self.request.body.decode("utf-8"))

        domain_model = booking_model.to_domain_model()

        result_booking = yield self.itinerary_service.book(domain_model)

        self.write(self.json_encoder.encode(result_booking.__dict__))
