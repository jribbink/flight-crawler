from datetime import datetime
import json

import yaml
from flight_api import Departure, get_departures

## read config
config = None
with open('./config.yaml', "r") as cfg:
  config = yaml.safe_load(cfg)

token = config["FLIGHTRADAR24_TOKEN"]                                 # api token
date = datetime(*[int(x) for x in str(config["DATE"]).split("/")])    # query departures for day (local timezone)

airports = [
	"YYJ",
	"YVR",
	"YXX",
	"YKA",
	"YLW",
	"YXS",
	"YXC",
	"YEG",
	"YYC",
	"YQU",
	"YQR",
	"YXE",
	"YBR",
	"YWG",
	"YHM",
	"YYZ",
	"YKF",
	"YOW",
	"YQT",
	"YUL",
	"YQB",
	"YFC",
	"YSJ",
	"YHZ",
	"YYG",
	"YYT",
	"YJT",
	"YDA",
	"YXY",
	"YZF"
]

departures: 'list[Departure]' = []
for a in airports:
  print("Getting departures from {}...".format(a))
  departures += [d for d in get_departures(a, date, token) if d.destination in airports]

with open("output.json", "w+") as f:
  json.dump([d.__dict__ for d in departures], f)


print("\n".join([str([d.time, d.origin, d.destination]) for d in departures]))