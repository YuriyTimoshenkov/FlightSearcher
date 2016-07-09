import tornado.ioloop
import tornado.web
import Controllers.itinerary_controller
import Controllers.authenticationController
import DomainModel.services
import Adapters.gds_service_adapter
import Adapters.itinerary_sql_repository
import utils.json_datetime_encoder
from tornado.options import options
import settings


def make_app():
    return tornado.web.Application([
        (
            r"/api/itinerary",
            Controllers.itinerary_controller.ItineraryController,
            dict(
                itinerary_service=DomainModel.services.ItineraryService(
                    Adapters.gds_service_adapter.GDSServiceAdapterMock(),
                    Adapters.itinerary_sql_repository.ItinerarySqlRepository(options.dbConnectionString)),
                json_encoder=utils.json_datetime_encoder.ComplexEncoder(),
                auth_key=options.authKey
            )),
        (r"/api/auth", Controllers.authenticationController.AuthenticationHandler),
    ], cookie_secret="MY_SECRET_COOKIE_KEY")


def main():
    # token = Common.authdecorator.generateToken("{test: 'test'}")
    # decryptedToken = Common.authdecorator.verifyAndDecryptToken(token)

    app = make_app()

    app.listen(8886)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
