from mitmproxy import http


class MockResponse:
    def __init__(self, url: str, status_code: int, body: str, content_type: str):
        self.url = url
        self.status_code = status_code
        self.body = body
        self.content_type = {"Content-Type": content_type}


class Events:
    def __init__(self, mock_data: MockResponse):
        self.mock_data = mock_data

    def request(self, flow: http.HTTPRequest) -> None:
        if self.mock_data.url in flow.request.url:
            flow.response = http.HTTPResponse.make(
                status_code=self.mock_data.status_code,
                content=self.mock_data.body,
                headers=self.mock_data.content_type
            )


class Litmus:
    def __init__(self, mock_data: MockResponse):
        self.mock_data = mock_data

    def request(self, flow: http.HTTPRequest) -> None:
        if self.mock_data.url in flow.request.url:
            flow.response = http.HTTPResponse.make(
                status_code=self.mock_data.status_code,
                content=self.mock_data.body,
                headers=self.mock_data.content_type
            )


j = """
{
  "success": true,
  "data": {
    "abyssToken": "W10=",
    "bookings": [
      {
        "orderNo": "SH-901066346",
        "serviceType": 3,
        "vehicleType": "bike",
        "vehicleBrand": null,
        "customer": {
          "id": 875014
        },
        "addresses": [
          {
            "serviceType": 3,
            "statusRoute": 0,
            "originNote": null,
            "destinationNote": null,
            "distance": 1.183,
            "fare": 18000,
            "originName": "Tokyo Skipjack",
            "originAddress": "Bulungan St No.16, RT.11/RW.7, Kramat Pela, Kebayoran Baru, South Jakarta City, Jakarta 12130, Indonesia",
            "destinationName": "Jl. Sisingamangaraja No. 2",
            "destinationAddress": "Jl. Sisingamangaraja No.2, RT.2/RW.1, Selong, Kec. Kby. Baru, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12120, Indonesia",
            "latLongOrigin": "-6.242616,106.795916",
            "latLongDestination": "-6.239125,106.798483",
            "routePolyline": "tfbe@asyjSg@JaABSACBC@qIEy@@gCDyACC?EEqF@mCCK??wA?yABuB@sCCa@N?l@?n@A`ACt@@rADrCBR?",
            "driverCloseLocation": ",",
            "actualFare": 12000,
            "driverCut": 34000
          }
        ],
        "driverId": 940437084,
        "statusBooking": 2,
        "voucherAmountCut": null,
        "totalCustomerPrice": 40000,
        "totalActualPrice": 12000,
        "totalPrice": 18000,
        "totalDistance": 1.183,
        "totalDriverCut": 34000,
        "activitySource": null,
        "driverCloseLocation": ",",
        "driverPickupLocation": ",",
        "paymentType": "0",
        "arrivalTime": null,
        "closingTime": null,
        "timeField": "2021-02-19T17:31:04+07:00",
        "flagBooking": null,
        "driverName": "Nich",
        "driverPhone": "+628126987866",
        "noPolisi": "B481YA",
        "serviceAreaId": 1,
        "allocationStrategy": "",
        "currencyCode": "",
        "countryCode": "ID"
      }
    ]
  },
  "errors": null
}
"""
litmus = """
{
  "data": [
    {
      "properties": {
        "enable_unified_orders_page": false
      },
      "exp_type": "experiment",
      "unit_type": "customer",
      "experiment": "exp_cp_tx_unified_orders_page",
      "variant": "treatment-1"
    },
    {
      "properties": {
        "enable_order_listing_entry_point": true
      },
      "exp_type": "experiment",
      "unit_type": "customer",
      "experiment": "exp_cp_order_listing_entry_point",
      "variant": "control"
    }
  ],
  "success": true,
  "errors": []
}
"""

mr = MockResponse("https://integration-api.gojekapi.com/v2/bookings/active?abyss_token=W10%3D", 200, j,
                  "application/json")

l = MockResponse("https://integration-api.gojekapi.com/litmus/run/experiments", 200, litmus, "application/json")
b = MockResponse("https://integration-api.gojekapi.com/litmus/public/run/experiments", 200, litmus, "application/json")
c = MockResponse("https://integration-api.gojekapi.com/litmus/public/run/experiment", 200, litmus, "application/json")

addons = [
    Events(mr),
    Litmus(l),
    Litmus(b),
    Litmus(c)
]
