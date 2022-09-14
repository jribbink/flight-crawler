from datetime import datetime, timedelta
import json
from urllib import request
from urllib.parse import urlencode

class Departure():
  def __init__(self, origin, data) -> None:
    self.time = data["flight"]["time"]["scheduled"]["departure"]
    self.origin = origin
    self.destination = data["flight"]["airport"]["destination"]["code"]["iata"]

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def get_departures(airport: str, day: datetime, token: str):
  start_date = day + timedelta(days=1)
  start_timestamp = int(datetime(start_date.year, start_date.month, start_date.day).timestamp())
  end_timestamp = start_timestamp - timedelta(days=1).microseconds * 1000

  def get_result(page = 1):
    resp = get_airport_schedule(airport, "departures", start_timestamp, page, token)

    departures_raw = resp["result"]["response"]["airport"]["pluginData"]["schedule"]["departures"]
    num_departures = int(departures_raw["item"]["total"])
    max_page = int(num_departures) // 100 + (num_departures % 100 > 0)
    departures = sorted([Departure(resp["result"]["request"]["code"], data) for data in departures_raw["data"]], key=lambda x: x.time, reverse=True)

    if(len(departures) > 0 and departures[-1].time > end_timestamp and page < max_page):
      return departures + get_result(page + 1)
    else:
      return [d for d in departures if d.time > end_timestamp]

  return sorted(get_result(), key=lambda x: x.time, reverse=True)

def get_airport_schedule(airport, mode, timestamp, page, token):
  params = {
    "code": airport,
    "plugin-setting[schedule][mode]": mode,
    "plugin-setting[schedule][timestamp]": timestamp,
    "page": page,
    "limit": 100,
    "token": token
  }
  url = "https://api.flightradar24.com/common/v1/airport.json?{}".format(urlencode(params, encoding="utf-8", safe="[]"))
  req = request.Request(
    url,
    headers={
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }
  )
  response = request.urlopen(req)

  return json.loads(response.read().decode('utf-8'))