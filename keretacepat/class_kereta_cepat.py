import json

import requests


class KeretaCepat:
    req_url = "https://ticket.kcic.co.id/ticket/ticketCache/query?"
    req_headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "appversion": "1.0.001",
        "appversioncode": "1",
        "deviceid": "00000000",
        "languagecode": "en_US",
        "platform": "web",
        "salemode": "E"
    }

    def __init__(self, train_date=None, from_station_telecode=None, to_station_telecode=None):
        self.req_params = {
            "trainDate": None,
            "fromStationTelecode": None,
            "toStationTelecode": None,
            "sortord": "1",
            "ticketFlag": "0",
            "startTimeInterval": "00:00-24:00"
        }
        self.req_params.update({"trainDate": train_date, "fromStationTelecode": from_station_telecode, "toStationTelecode": to_station_telecode})
        self.response = None

    def get_train_schedule(self) -> dict:
        return json.loads(requests.get(url=self.req_url, params=self.req_params, headers=self.req_headers, data=None, verify=False).text)

    def is_available(self) -> bool:
        self.response = self.get_train_schedule()
        return True if self.response["data"] else False


""" DEBUG
booking_date = "20231220"
from_station = "IDHMA"
to_station = "IDPGA"
if __name__ == "__main__":
    kereta = KeretaCepat(train_date=booking_date, from_station_telecode=from_station, to_station_telecode=to_station)
    print(f"Available = {kereta.is_available()}")
"""
