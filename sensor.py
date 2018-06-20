# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse

from influxdb import InfluxDBClient


def insert():
    user = 'root'
    password = 'root'
    dbname = 'example'
    query = 'select * from fog;'
    json_body = [
        {
            "measurement": "fog",
            "tags": {
                "host": "fog",
                "region": "us-west"
            },
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
    ]

    client = InfluxDBClient("192.168.11.32", 8086, user, password, dbname)

    print("Write points: {0}".format(json_body))
    print(client.write_points(json_body))


def get():
    user = 'root'
    password = 'root'
    dbname = 'example'
    query = 'select String_value from fog;'

    client = InfluxDBClient("192.168.11.32", 8086, user, password, dbname)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)

def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'root'
    password = 'root'
    dbname = 'example'
    query = 'select * from fog;'
    json_body = [
        {
            "measurement": "fog",
            "tags": {
                "host": "fog",
                "region": "us-west"
            },
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Write points: {0}".format(json_body))
    print(client.write_points(json_body))

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    result = client.query('select Int_value from fog')

    print("Result: {0}".format(result))

if __name__ == '__main__':
    # main(host="192.168.11.32", port=8086)
    insert()
    get()
