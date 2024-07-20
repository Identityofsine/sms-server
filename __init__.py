import threading
import os
import asyncio
import json
from datetime import datetime as Date
from model.device import Device, ConnectedDevice
from bt.pbap import createPBAPSession
from bt.map import createMAPSession

async def main_thread():
	os.system("clear")
	d = Device("78:FB:D8:94:FC:68", "kevin's Iphone")
	n = await d.attempt_connect()
	while n is None:
		print(f"Failed to connect to device {d.name} at address {d.address}, trying again in 5 seconds")
		n = await d.attempt_connect()
		await asyncio.sleep(5)	
		pass

	#while True:
		#sleep thread
		#print(n.mailbox.to_string())


def main():
	asyncio.get_event_loop().create_task(main_thread())
	loop = asyncio.get_event_loop()
	loop.run_forever()
	pass

main()

	


