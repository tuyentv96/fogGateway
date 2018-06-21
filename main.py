from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from src.influxdb.db import *
import sys
import logging
from src.mqtt.mqtt import *
import serial

class uartThread(QThread):
	updateUartData = pyqtSignal(dict, name="updateUartData")

	def __init__(self):
		super(uartThread, self).__init__()
		# GPIO.setmode(GPIO.BOARD)
		# GPIO.setup(16, GPIO.OUT)
		# GPIO.setup(18, GPIO.OUT)
		# GPIO.output(16, False)
		# GPIO.output(18, False)

		self.ser = serial.Serial(
			port='/dev/tty.SLAB_USBtoUART',
			baudrate=9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
		)

	def run(self):
		print("Started")
		buffer = ""
		while True:
			data = self.ser.readline().decode('ascii')
			if data:
				print("serial readline:"+str(data))
				part=data.split("/")
				print(part)
				sensor={}
				sensor["id"]=1
				sensor["temp"]=int(float(part[0]))
				sensor["humd"]=int(float(part[1]))
				sensor["pm25"]=int(part[2])
				self.updateUartData.emit(sensor)

class mainThread (QThread):
	def __init__(self):
		super(mainThread, self).__init__()
		#createDB()
		self.mqtt=mqttConnectClass()
		self.mqtt.start()
		self.uart=uartThread()
		self.uart.start()

		self.uart.updateUartData.connect(self.uartdownlink)
		self.mqtt.downlinkSignal.connect(self.downlink)
		data={}
		data['id']=1
		data['temp']=2
		data['humd']=3
		data['pm25']=5
		try:
			insert(data)
			get(data)
			getAll()
			print(list(getLast().get_points()))
			list(getInDay().get_points())
		except Exception as e:
			print("influxdb error")
			print(e)

	def uartdownlink(self,payload):
		print("uart downlink")
		insert(payload)
	def downlink(self,payload):
		print("uplink:"+str(payload))
		if payload["cmd"]==1:
			print("cmd=1")
			data=getInDay()
			print("Da:"+str(list(data.get_points())))
			ds={}
			ds["last"]=list(getLast().get_points())[0]
			ds["avg"]=list(getAvg().get_points())[0]
			ds["min"]=list(getMin().get_points())[0]
			ds["max"]=list(getMax().get_points())[0]
			ds["chart"]=list(getInDay().get_points())

			respone={}
			respone["cmd"]=1
			respone["id"]="node1"
			respone["data"]=ds
			self.mqtt.uplinkSignal.emit(respone)

def main():
	app = QCoreApplication(sys.argv)
	mMainThread = mainThread()
	mMainThread.start()
	sys.exit(app.exec_())

main()

