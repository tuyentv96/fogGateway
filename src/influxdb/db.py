from influxdb import InfluxDBClient
import time
import datetime
DB_HOST="192.168.10.83"
PORT=8086
USER = 'root'
PASSWORD = 'root'
DBNAME = 'fogdb'


def createDB():
    client = InfluxDBClient(DB_HOST,PORT, USER, PASSWORD, DBNAME)
    client.create_database(DBNAME)

def insert(data):
    json_body = [
        {
            "measurement": DBNAME,
            "tags": {
                "id": data['id']
            },
            "time":  datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "temp": data['temp'],
                "humd": data['humd'],
                "pm25": data['pm25']
            }
        }
    ]

    client = InfluxDBClient(DB_HOST,PORT, USER, PASSWORD, DBNAME)

    print("Write points: {0}".format(json_body))
    print(client.write_points(json_body))

def get(input):
    query = 'select last(temp) as temp,last(humd) as humd,last(pm25) as pm25 from fogdb '

    client = InfluxDBClient(DB_HOST, PORT, USER, PASSWORD, DBNAME)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    return result


def getAll():
    query = 'select * from fogdb '

    client = InfluxDBClient(DB_HOST, PORT, USER, PASSWORD, DBNAME)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    return result

def getInDay():
    query = 'select temp,humd,pm25 from fogdb where time > now() - 1d GROUP BY time(1h)'

    client = InfluxDBClient(DB_HOST, PORT, USER, PASSWORD, DBNAME)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    return result