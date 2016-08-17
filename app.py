import tornado.ioloop
import tornado.web
import Controllers.itinerary_controller
import Controllers.authentication_controller
import Controllers.airports_controller
import DomainModel.services
import Adapters.gds_service_adapter
import Adapters.itinerary_sql_repository
import Adapters.airports_repository
import utils.json_datetime_encoder
from tornado.options import options
import settings
import logging
import logging.config

logging.config.fileConfig('logging.conf')


def make_app():
    app = tornado.web.Application([
        (
            r"/api/itinerary",
            Controllers.itinerary_controller.ItineraryController,
            dict(
                itinerary_service=DomainModel.services.ItineraryService(
                    Adapters.gds_service_adapter.SabreGDSServiceAdapter(Adapters.gds_service_adapter.SabreProxyMock),
                    Adapters.itinerary_sql_repository.ItinerarySqlRepository(options.dbConnectionString),
                    logging.getLogger('FSLogger'),
                    utils.json_datetime_encoder.ComplexEncoder()),
                json_encoder=utils.json_datetime_encoder.ComplexEncoder(),
                auth_key=options.authKey,
                logger=logging.getLogger('FSLogger')
            )),
        (r"/api/auth", Controllers.authentication_controller.AuthenticationHandler),
        (
            r"/api/lookup/airports/query/([A-Z]+)", Controllers.airports_controller.AirportsController,
            dict(
                airports_repository = Adapters.airports_repository.AirportsRepository(options.airportSourceAuthKey, options.airportsSourceUrl)
            )
        )
    ], cookie_secret="MY_SECRET_COOKIE_KEY")

    app.logger = logging.getLogger('FSLogger')

    return app


def main():
    # token = Common.authdecorator.generateToken("{test: 'test'}")
    # decryptedToken = Common.authdecorator.verifyAndDecryptToken(token)

    app = make_app()

    app.listen(8886)

    app.logger.info('Application lunched.')

    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
