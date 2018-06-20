import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform
import socket

connflag = False
from PyQt5.QtCore import *
import threading


def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


class mqttConnectClass(QThread):
    uplinkSignal    =   pyqtSignal(str, name="uplinkSignal")
    downlinkSignal    =   pyqtSignal(str, name="downlinkSignal")

    def __init__(self):
        super(mqttConnectClass, self).__init__()
        self._mqttc = paho.Client()
        # self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe
        self.clientid = "123"
        self.connected = False
        self.keepRunning = True

        awshost = '203.162.76.52'
        awsport = 4025
        clientId = "12345678"
        thingName = "myThingName"
        self._mqttc.connect(awshost, awsport, keepalive=60)

        # self._mqttc.loop_start()

    def mqtt_on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def publish(self, topic, msg):
        self._mqttc.publish(topic, msg)

    def Sub_All(self):
        self._mqttc.subscribe("#", 0)

    def subscribe(self, topic):
        self._mqttc.subscribe(topic, 0)

    def run(self):
        try:
            self._mqttc.connect("203.162.76.52", 4025, 60)
            print("DB1")
            self.connected = True
        except:
            print("No connection")
            self.connected = False
            self.keepRunning = False
            return None

        self.keepRunning = True
        self._mqttc.loop_forever()
        # self.Sub_All()
        # while self.keepRunning:
        #     self._mqttc.loop()
        rc = 0
        while rc == 0:
            rc = self._mqttc.loop_start()
        # return rc
        # while self.keepRunning:
        #     time.sleep(1)
        self.connected = False
        self.keepRunning = False
        print("Loop done !!!")