from typing import Callable
from .mailbox import Mailbox
from .contact import ContactBook
import threading
import os
import asyncio
from util.log import log
from bt.pbap import createPBAPSession
from bt.map import createMAPSession
from bt.pair import connect, get_device_name 

class Device:
	address:str 
	name:str
	src:str = "Device"

	def __init__(self, address:str, name:str):
		self.address = address
		self.name = name
	
	async def attempt_connect(self): 
		#connect to device
		mb = None
		try:
			log(f"Attempting to connect to device {self.name} at address {self.address}")
			if connect(self.address):
				log(f"[{self.src}] Connected to device {self.name} at address {self.address}")
				ConnectedDevice.init__pbap(self.address)
				msg = createMAPSession(self.address)
				log(f"[{self.src}] Connected to MAP session")
				msgs = msg()
				log(f"[{self.src}] Connected to OBEX session")
				mb = Mailbox.from_obex(msgs)
				while mb is None:
					log(f"[{self.src}] Failed to connect to device {self.name} at address {self.address}, trying again in 2 seconds")
					threading.Event().wait(2)
					mb = Mailbox.from_obex(msgs)
				return ConnectedDevice(self.address, get_device_name(self.address), mb, msg)
			else:
				log(f"[{self.src}] Failed to connect to device {self.name} at address {self.address}")
				return None
		except Exception as e:
			log(f"[{self.src}::attempt_connect] {e}")
			return None

class ConnectedDevice(Device):
	mailbox: Mailbox
	contactbook: ContactBook
	connection: bool = True
	poll: Callable

	def __init__(self, address:str, name:str, mailbox:Mailbox, poll: Callable):
		super().__init__(address, name)
		log(f"[ConnectedDevice] Connected to device {name} at address {address}")
		self.mailbox = mailbox
		self.poll = poll
		self.contactbook = None 
		asyncio.create_task(self.start_poll())


	async def attempt_reconnect(self):
		log(f"[ConnectedDevice] Attempting to reconnect to device {self.name} at address {self.address}")
		new = await self.attempt_connect()	
		while new is None:
			log(f"[ConnectedDevice] Failed to reconnect to device {self.name} at address {self.address}, trying again in 5 seconds")
			await asyncio.sleep(5)
			new = await self.attempt_connect()
		self = new

	
	async def start_poll(self):
		try:
			while self.connection:
				await asyncio.sleep(5)
				self.mailbox.update(self.poll())
		except Exception as e:
			log(f"[ConnectedDevice::start_poll] {e}")
			self.connection = False
			await self.attempt_reconnect()
	
	#private
	@staticmethod
	def init__pbap(address:str):
		try:
			if not os.path.exists("/opt/pybt/"):
				os.mkdir("/opt/pybt/")
			if not os.path.exists("/opt/pybt/phonebook.vcf"):
				log("[ConnectedDevice] Creating phonebook file")
				createPBAPSession(address)("/opt/pybt/phonebook.vcf", {})
				if os.path.exists("/opt/pybt/phonebook.vcf"):
					log("[ConnectedDevice::init__pbap] Success!")
			return True
		except Exception as e:
			if isinstance(e, PermissionError):
				log("[ConnectedDevice::init__pbap] Failed! - Please create /opt/pybt/ directory and try again (make sure you have write permissions)")
			else:
				log(f"[ConnectedDevice::init__pbap] Failed! - {e}")
			return False

	def update_mailbox(self, obex_msg: dict):
		self.mailbox.update(obex_msg)
		pass

