import unittest
import Adapters.gds_service_adapter
import DomainModel.models
import datetime


class GDSServiceAdapterTest(unittest.TestCase):
    def test_search(self):
        adapter = Adapters.gds_service_adapter.GDSServiceAdapterMock()

        search_request = DomainModel.models.ItinerarySearchRequest(
            "KIV", "NYC",
            datetime.datetime.now(), datetime.datetime.now(),
            True)

        result = adapter.search(search_request)

        self.assertTrue(result[1].Price == '136.20 USD')
