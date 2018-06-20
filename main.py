from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from src.influxdb.db import *
import sys
import logging
from src.mqtt.mqtt import *

class mainThread (QThread):
	def __init__(self):
		super(mainThread, self).__init__()
		#createDB()
		self.mqtt=mqttConnectClass()
		self.mqtt.start()
		data={}
		data['id']=1
		data['temp']=2
		data['humd']=3
		data['pm25']=5
		try:
			insert(data)
			get(data)
			getAll()
		except:
			print("influxdb error")

	def uplink(self,payload):
		print("uplink:"+str(payload))

def main():
	app = QCoreApplication(sys.argv)
	mMainThread = mainThread()
	mMainThread.start()
	sys.exit(app.exec_())

main()

