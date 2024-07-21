import threading
import os
import asyncio
import json
from datetime import datetime as Date
from typing import overload
from model.device import Device, ConnectedDevice
from bt.pbap import createPBAPSession
from bt.map import createMAPSession
from bt.reboot import reboot_bluetooth, reboot_obex
from db.database import Database, DeviceInfo



def arg_handler():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--device", help="Device address to connect to", type=str)
	parser.add_argument("-D", "--debug", help="Enable verbose logging", action="store_true")
	parser.add_argument('-r', "--reboot", help="Reboot Bluetooth Service", action="store_true")
	args = parser.parse_args()
	return args

async def main_thread(args):
	
	os.system("clear")

	if args.device is None:
		print("No device address provided, exiting")
		asyncio.get_event_loop().stop()
		return

	if args.reboot:
		await reboot_bluetooth()
		await reboot_obex()


	db = Database.get_instance()
  #"78:FB:D8:94:FC:68"
	d = Device(args.device, "?")
	n = await d.attempt_connect()
	while n is None:
		print(f"Failed to connect to device {d.name} at address {d.address}, trying again in 5 seconds")
		n = await d.attempt_connect()
		await asyncio.sleep(5)		
	#while True:
		#sleep thread
		#print(n.mailbox.to_string())
	db.add_device(DeviceInfo.from_device(n))

def main():
	args = arg_handler()
	asyncio.get_event_loop().create_task(main_thread(args))
	loop = asyncio.get_event_loop()
	loop.run_forever()
	pass

main()

	


