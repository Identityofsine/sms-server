import threading
import os
from datetime import datetime as Date
from model.device import Device, ConnectedDevice
from bt.pbap import createPBAPSession
from bt.map import createMAPSession


os.system("clear")
d = Device("78:FB:D8:94:FC:68", "kevin's Iphone")
n = d.attempt_connect()
while n is None:
	print(f"Failed to connect to device {d.name} at address {d.address}, trying again in 5 seconds")
	n = d.attempt_connect()
	threading.Event().wait(5)
	pass

while True:
	#sleep thread
	print(n.mailbox.to_json())
	


