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
	db = Database.get_instance()

	# if --device is not provided, list devices and ask for input
	if args.device is None:
		devices = db.get_devices()
		print('--Devices--')
		if len(devices) == 0:
			print("No devices found")
		else:
			for d in devices:
				print(f"{d.name} - {d.address}")
		print("Enter device address to connect to:")
		args.device = input("")
		#TODO: fix and add pairing
		if args.device not in [d.address for d in devices]:
			print("Invalid device address provided, TODO: add pairing")
			asyncio.get_event_loop().stop()
			return
		elif args.device == "": # can look better
			print("No device address provided, exiting...")
			asyncio.get_event_loop().stop()
			return
		else:
			pass

	if args.reboot:
		await reboot_bluetooth()
		await reboot_obex()


  #"78:FB:D8:94:FC:68" - my iphone 
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

	


