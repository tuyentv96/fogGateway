from influxdb import InfluxDBClient
import time
import datetime
DB_HOST="127.0.0.1"
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
            "fields": {
                "time": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
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

def getLast():
    query = 'select last(temp) as temp,last(humd) as humd,last(pm25) as pm25 from fogdb'

    client = InfluxDBClient(DB_HOST, PORT, USER, PASSWORD, DBNAME)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    return result
def getMin():
    query = 'select min(temp) as temp,min(humd) as humd,min(pm25) as pm25 from fogdb where time > now() - 10d '

    client = InfluxDBClient(DB_HOST, PORT, USER, PASSWORD, DBNAME)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    return result
def getMax():
    query = 'select MEAN(temp) as temp,MEAN(humd) as humd,MEAN(pm25) as pm25 from fogdb where time > now() - 1d GROUP BY time(1h)'
    query = 'select max(temp) as temp,max(humd) as humd,max(pm25) as pm25 from fogdb where time > now() - 10d '

    client = InfluxDBClient(DB_HOST, PORT, USER, PASSWORD, DBNAME)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    return result
def getAvg():
    query = 'select MEAN(temp) as temp,MEAN(humd) as humd,MEAN(pm25) as pm25 from fogdb where time > now() - 1d GROUP BY time(1h)'
    query = 'select mean(temp) as temp,mean(humd) as humd,mean(pm25) as pm25 from fogdb where time > now() - 10d '

    client = InfluxDBClient(DB_HOST, PORT, USER, PASSWORD, DBNAME)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    return result

def getInDay():
    # query = 'select COUNT(temp) as temp,COUNT(humd) as humd,COUNT(pm25) as pm25 from fogdb where time > now() - 1h GROUP BY time(1m)'
    # query = 'select last(temp) from fogdb where time > now() - 10d '
    query = 'select mean(temp) as temp,mean(humd) as humd,mean(pm25) as pm25  from fogdb where time > now() - 1d GROUP BY time(60m)'
    client = InfluxDBClient(DB_HOST, PORT, USER, PASSWORD, DBNAME)

    print("Querying data: " + query)
    result = client.query(query)

    print(result)
    return result