# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
import adafruit_dht

from prometheus_client import Gauge
from prometheus_client import start_http_server


if __name__ == "__main__":
    # Start prometheus server.
    start_http_server(1234)

    # Initialize the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT11(board.D4)

    # Configure temperature and humidity gauge metrics.
    temp_gauge = Gauge('temp', 'Description of gauge')
    humidity_gauge = Gauge('humidity', 'Description of gauge')

    while True:
        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32

            humidity = dhtDevice.humidity

            temp_gauge.set(temperature_f)
            humidity_gauge.set(humidity)
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        time.sleep(60)