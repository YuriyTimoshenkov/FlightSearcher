import json

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado import gen

import DomainModel.models
import datetime


class SabreProxyMock:
    mocked_gds_response = """{"PricedItineraries":[{"AirItinerary":{"OriginDestinationOptions":{"OriginDestinationOption":[{"FlightSegment":[{"DepartureAirport":{"LocationCode":"ORD"},"ArrivalAirport":{"LocationCode":"LGA"},"MarketingAirline":{"Code":"NK"},"ArrivalTimeZone":{"GMTOffset":-4},"TPA_Extensions":{"eTicket":{"Ind":true}},"StopQuantity":0,"ElapsedTime":124,"ResBookDesigCode":"U","MarriageGrp":"O","Equipment":{"AirEquipType":320},"DepartureDateTime":"2015-04-13T05:56:00","ArrivalDateTime":"2015-04-13T09:00:00","FlightNumber":224,"OnTimePerformance":{"Level":6},"OperatingAirline":{"FlightNumber":224,"Code":"NK"},"DepartureTimeZone":{"GMTOffset":-5}}],"ElapsedTime":124},{"FlightSegment":[{"DepartureAirport":{"LocationCode":"LGA"},"ArrivalAirport":{"LocationCode":"ORD"},"MarketingAirline":{"Code":"NK"},"ArrivalTimeZone":{"GMTOffset":-5},"TPA_Extensions":{"eTicket":{"Ind":true}},"StopQuantity":0,"ElapsedTime":137,"ResBookDesigCode":"U","MarriageGrp":"O","Equipment":{"AirEquipType":320},"DepartureDateTime":"2015-04-20T21:55:00","ArrivalDateTime":"2015-04-20T23:12:00","FlightNumber":331,"OnTimePerformance":{"Level":3},"OperatingAirline":{"FlightNumber":331,"Code":"NK"},"DepartureTimeZone":{"GMTOffset":-4}}],"ElapsedTime":137}]},"DirectionInd":"Return"},"TPA_Extensions":{"ValidatingCarrier":{"Code":"NK"}},"SequenceNumber":1,"AirItineraryPricingInfo":{"PTC_FareBreakdowns":{"PTC_FareBreakdown":{"FareBasisCodes":{"FareBasisCode":[{"BookingCode":"U","DepartureAirportCode":"ORD","AvailabilityBreak":true,"ArrivalAirportCode":"LGA","content":"UA7Y4"},{"BookingCode":"U","DepartureAirportCode":"LGA","AvailabilityBreak":true,"ArrivalAirportCode":"ORD","content":"UA7Y4"}]},"PassengerTypeQuantity":{"Quantity":1,"Code":"ADT"},"PassengerFare":{"FareConstruction":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46},"TotalFare":{"CurrencyCode":"USD","Amount":"136.20"},"Taxes":{"TotalTax":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":35.74},"Tax":[{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"US1","Amount":7.54},{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"ZP","Amount":"8.00"},{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"AY","Amount":"11.20"},{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"XF","Amount":"9.00"}]},"BaseFare":{"CurrencyCode":"USD","Amount":100.46},"EquivFare":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46}}}},"FareInfos":{"FareInfo":[{"TPA_Extensions":{"Cabin":{"Cabin":"Y"},"SeatsRemaining":{"BelowMin":false,"Number":4}},"FareReference":"U"},{"TPA_Extensions":{"Cabin":{"Cabin":"Y"},"SeatsRemaining":{"BelowMin":false,"Number":4}},"FareReference":"U"}]},"TPA_Extensions":{"DivideInParty":{"Indicator":false}},"ItinTotalFare":{"FareConstruction":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46},"TotalFare":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":"136.20"},"Taxes":{"Tax":[{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"TOTALTAX","Amount":35.74}]},"BaseFare":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46},"EquivFare":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46}}},"TicketingInfo":{"TicketType":"eTicket"}},{"AirItinerary":{"OriginDestinationOptions":{"OriginDestinationOption":[{"FlightSegment":[{"DepartureAirport":{"LocationCode":"ORD"},"ArrivalAirport":{"LocationCode":"LGA"},"MarketingAirline":{"Code":"NK"},"ArrivalTimeZone":{"GMTOffset":-4},"TPA_Extensions":{"eTicket":{"Ind":true}},"StopQuantity":0,"ElapsedTime":124,"ResBookDesigCode":"U","MarriageGrp":"O","Equipment":{"AirEquipType":320},"DepartureDateTime":"2015-04-13T05:56:00","ArrivalDateTime":"2015-04-13T09:00:00","FlightNumber":224,"OnTimePerformance":{"Level":6},"OperatingAirline":{"FlightNumber":224,"Code":"NK"},"DepartureTimeZone":{"GMTOffset":-5}}],"ElapsedTime":124},{"FlightSegment":[{"DepartureAirport":{"LocationCode":"LGA"},"ArrivalAirport":{"LocationCode":"ORD"},"MarketingAirline":{"Code":"NK"},"ArrivalTimeZone":{"GMTOffset":-5},"TPA_Extensions":{"eTicket":{"Ind":true}},"StopQuantity":0,"ElapsedTime":149,"ResBookDesigCode":"U","MarriageGrp":"O","Equipment":{"AirEquipType":320},"DepartureDateTime":"2015-04-20T08:35:00","ArrivalDateTime":"2015-04-20T10:04:00","FlightNumber":847,"OnTimePerformance":{"Level":4},"OperatingAirline":{"FlightNumber":847,"Code":"NK"},"DepartureTimeZone":{"GMTOffset":-4}}],"ElapsedTime":149}]},"DirectionInd":"Return"},"TPA_Extensions":{"ValidatingCarrier":{"Code":"NK"}},"SequenceNumber":2,"AirItineraryPricingInfo":{"PTC_FareBreakdowns":{"PTC_FareBreakdown":{"FareBasisCodes":{"FareBasisCode":[{"BookingCode":"U","DepartureAirportCode":"ORD","AvailabilityBreak":true,"ArrivalAirportCode":"LGA","content":"UA7Y4"},{"BookingCode":"U","DepartureAirportCode":"LGA","AvailabilityBreak":true,"ArrivalAirportCode":"ORD","content":"UA7Y4"}]},"PassengerTypeQuantity":{"Quantity":1,"Code":"ADT"},"PassengerFare":{"FareConstruction":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46},"TotalFare":{"CurrencyCode":"USD","Amount":"136.20"},"Taxes":{"TotalTax":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":35.74},"Tax":[{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"US1","Amount":7.54},{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"ZP","Amount":"8.00"},{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"AY","Amount":"11.20"},{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"XF","Amount":"9.00"}]},"BaseFare":{"CurrencyCode":"USD","Amount":100.46},"EquivFare":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46}}}},"FareInfos":{"FareInfo":[{"TPA_Extensions":{"Cabin":{"Cabin":"Y"},"SeatsRemaining":{"BelowMin":false,"Number":4}},"FareReference":"U"},{"TPA_Extensions":{"Cabin":{"Cabin":"Y"},"SeatsRemaining":{"BelowMin":false,"Number":4}},"FareReference":"U"}]},"TPA_Extensions":{"DivideInParty":{"Indicator":false}},"ItinTotalFare":{"FareConstruction":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46},"TotalFare":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":"136.20"},"Taxes":{"Tax":[{"CurrencyCode":"USD","DecimalPlaces":2,"TaxCode":"TOTALTAX","Amount":35.74}]},"BaseFare":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46},"EquivFare":{"CurrencyCode":"USD","DecimalPlaces":2,"Amount":100.46}}},"TicketingInfo":{"TicketType":"eTicket"}}],"ReturnDateTime":"2015-04-20","DepartureDateTime":"2015-04-13","DestinationLocation":"LGA","OriginLocation":"ORD","Links":[{"rel":"nextResults","href":"https://api.sabre.com/v1/shop/flights?origin=ORD&destination=LGA&departured…4-20&maxfare=140&limit=2&passengercount=4&outboundstopduration=30&offset=3"},{"rel":"self","href":"https://api.sabre.com/v1/shop/flights?origin=ORD&destination=LGA&departured…te=2015-04-20&maxfare=140&limit=2&passengercount=4&outboundstopduration=30"},{"rel":"linkTemplate","href":"https://api.sabre.com/v1/shop/flights?origin=<origin>&destination=<destination>&departuredate=<departuredate>&returndate=<returndate>&offset=<offset>&limit=<limit>&sortby=<sortby>&order=<order>&sortby2=<sortby2>&order2=<order2>&minfare=<minfare>&maxfare=<maxfare>&includedcarriers=<includedcarriers>&excludedcarriers=<excludedcarriers>&outboundflightstops=<outboundflightstops>&inboundflightstops=<inboundflightstops>&outboundstopduration=<outboundstopduration>&inboundstopduration=<inboundstopduration>&outbounddeparturewindow=<outbounddeparturewindow>&outboundarrivalwindow=<outboundarrivalwindow>&inbounddeparturewindow=<inbounddeparturewindow>&inboundarrivalwindow=<inboundarrivalwindow>&onlineitinerariesonly=<onlineitinerariesonly>&eticketsonly=<eticketsonly>&includedconnectpoints=<includedconnectpoints>&excludedconnectpoints=<excludedconnectpoints>&pointofsalecountry=<pointofsalecountry>&passengercount=<passengercount>"}]}"""

    def insta_flight_search(self, itinerary_search_request):
        return SabreProxyMock.mocked_gds_response


class SabreProxy:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    @gen.coroutine
    def insta_flight_search(self, itinerary_search_request):
        http_client = AsyncHTTPClient()

        url = self.base_url + ('?origin={}&destination={}&departuredate={:%Y-%m-%d}&returndate={:%Y-%m-%d}'.format(
                    itinerary_search_request.origin,
                    itinerary_search_request.destination,
                    itinerary_search_request.departure_date,
                    itinerary_search_request.return_date))

        response = yield http_client.fetch(HTTPRequest(
            url,
            'GET',
            {
                'Authorization': self.auth_token
            }))

        return response.body.decode("utf-8")


class SabreGDSServiceAdapter:
    def __init__(self, proxy_client):
        self.proxy_client = proxy_client

    @gen.coroutine
    def search(self, itinerary_search_request):
        gds_response = yield self.proxy_client.insta_flight_search(itinerary_search_request)

        parsed_response = json.loads(gds_response)

        itineraries = parsed_response['PricedItineraries']
        result = list(map(SabreGDSServiceAdapter.parse_priced_itinerary, itineraries))

        return result

    def book(self, itinerary):
        return

    @staticmethod
    def parse_priced_itinerary(priced_itinerary):
        result = DomainModel.models.ItinerarySearchResult()
        result.BookingDate = datetime.datetime.now()
        result.Owner = "None"

        total_fare = priced_itinerary['AirItineraryPricingInfo']['ItinTotalFare']['TotalFare']
        result.Price = total_fare['Amount']# + ' ' + total_fare['CurrencyCode']

        result.Segments = list(map(SabreGDSServiceAdapter.parse_itinerary, priced_itinerary['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption']))

        index = 1
        for segment in result.Segments:
            segment.Id = index
            index += 1

        return result

    @staticmethod
    def parse_itinerary(itinerary):
        result = DomainModel.models.ItinerarySegment()
        segment = itinerary['FlightSegment'][0]

        result.Origin = segment['DepartureAirport']['LocationCode']
        result.Destination = segment['ArrivalAirport']['LocationCode']
        result.Duration = segment['ElapsedTime']
        result.FlightStopsCount = segment['StopQuantity']
        result.FlightNumber = segment['FlightNumber']

        return result



