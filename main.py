#!/usr/bin/python3
# Simple example of reading the MCP3008 analog input channels using its
# Author: Gabriel Rodriguez
# License: MIT
# To Add Delay
import time
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
# Scale Values
from numpy import interp
# Import DateTime
import datetime
# Import Elasticsearch Libraries
from elasticsearch import Elasticsearch
# Import Requests library to figure out external IP address
import requests
# Import netifaces library to figure out the internal IP address
import netifaces as ni
# Import socket library to get figure out the hostname
import socket
# Import Pretty Printer for JSON & Python Dictionaries
# from prettyprinter import pprint
# Generate Random IDs
import uuid
# Localize the timestamp
import pytz


# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def main():
    # Build Elasticsearch client
    es = Elasticsearch('IPADDRESS:9200') # IP ADDRESS or Elasticsearch Target URL goes here.
    # Get Internal
    #  IP Address and save it as the variable 'hip'
    ni.ifaddresses('wlan0')
    hip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    # Get External IP address and save it as the variable 'exip'
    exip = requests.get('http://icanhazip.com/')
    # Get the Hostname of this Raspberry Pi
    hname = socket.gethostname()

    # The read_adc function will get the value of the specific channel (0-7).
    value0  = mcp.read_adc(0)
    scale0  = interp(value0, [433, 1023], [100, 0])
    output0 = int(scale0)

    value1  = mcp.read_adc(1)
    scale1  = interp(value1, [432, 1023], [100, 0])
    output1 = int(scale1)


    channel0_sample    = int('{0}'.format(value0))
    channel1_sample    = int('{0}'.format(value1))
    channel0_percent   = int('{0}'.format(output0))
    channel1_percent   = int('{0}'.format(output1))
    timestamp          = datetime.datetime.now(datetime.timezone.utc).isoformat()

    doc = {
        'hostname' : hname,
        'internal IP' :hip,
        'external IP' : str(exip.text).strip(),
        'channel 0 Sample' : channel0_sample,
        'channel 0 Moisture Percentage' : channel0_percent,
        'channel 1 Sample' : channel1_sample,
        'channel 1 Moisture Percentage' : channel1_percent,
        'timestamp': timestamp
    }
    random_id=uuid.uuid4()
    res = es.index(index="soil-index", id=random_id, body=doc)
    print(res['result'])

    res = es.get(index="soil-index", id=random_id)
    print(res['_source'])

if __name__ == "__main__":
    main()
