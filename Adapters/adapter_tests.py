import unittest

import tornado
from tornado.testing import AsyncTestCase

import Adapters.gds_service_adapter
import DomainModel.models
import datetime


class GDSServiceAdapterTest(AsyncTestCase):
    @tornado.testing.gen_test
    def test_search_mocked_proxy(self):
        adapter = Adapters.gds_service_adapter.SabreGDSServiceAdapter(Adapters.gds_service_adapter.SabreProxyMock())

        search_request = DomainModel.models.ItinerarySearchRequest(
            "KIV", "NYC",
            datetime.datetime.now(), datetime.datetime.now(),
            True)

        result = yield adapter.search(search_request)

        self.assertTrue(result[1].Price == '136.20')

    @tornado.testing.gen_test
    def test_search_live_proxy(self):
        adapter = Adapters.gds_service_adapter.SabreGDSServiceAdapter(Adapters.gds_service_adapter.SabreProxy(
            'https://api.test.sabre.com/v1/shop/flights',
            'Bearer T1RLAQJYvGz/aSMERPndAtFH+fRU648JXxChElf1l3KbwbKJaJEMXIRWAACgYT908ORYxC+kR6Z0Br82oJeRtt0It4V7fmgaAzEr1+GRdwZ39LWFN0ZfBHYx5R/pfExjkLKsW7n+UH4OS9BfxC7RZ20J4YoJPF60Ls+sKndal2bvYCzgJaj/Fji2QuqgBu4Z/JKirZFNeXsmDtiDFzet/21h493FUdsa79pfhe/8BRmr41tLR7QDGPcbfn74FH90q66560ssx4ohdvqxDA**'
        ))

        search_request = DomainModel.models.ItinerarySearchRequest(
            "JFK", "LAX",
            datetime.date(2016, 10, 7), datetime.date(2016, 10, 8),
            True)

        result = yield adapter.search(search_request)

        self.assertTrue(float(result[1].Price) > 0)
