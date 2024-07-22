from typing import Callable
from .mailbox import Mailbox
from .contactbook import ContactBook
import threading
import os
import asyncio
from util.log import log
from bt.pbap import createPBAPSession
from bt.map import createMAPSession
from bt.pair import connect, get_device_name 


POLL_RATE = 2.5
RETRY_RATE = 5

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
				mb = Mailbox.from_obex(msgs, None)
				while mb is None:
					log(f"[{self.src}] Failed to connect to device {self.name} at address {self.address}, trying again in 2 seconds")
					threading.Event().wait(2)
					mb = Mailbox.from_obex(msgs, None)
				return ConnectedDevice(self.address, get_device_name(self.address), mb, msg)
			else:
				log(f"[{self.src}] Failed to connect to device {self.name} at address {self.address}")
				return None
		except Exception as e:
			log(f"[{self.src}::attempt_connect] {e}")
			return None

class ConnectedDevice(Device):
	__pbap_dir = f"{os.path.dirname(os.path.realpath(__file__))}/../data/"
	__pbap_file = f"raise"
	mailbox: Mailbox
	contactbook: ContactBook | None
	connection: bool = True
	poll: Callable

	def __init__(self, address:str, name:str, mailbox:Mailbox, poll: Callable):
		super().__init__(address, name)
		log(f"[ConnectedDevice] Connected to device {name} at address {address}")
		self.mailbox = mailbox
		self.poll = poll
		self.__pbap_file = f"phonebook_{self.address.replace(":", "_")}.vcf"
		self.contactbook = ContactBook.from_vcard(ConnectedDevice.__pbap_dir + self.__pbap_file) 
		asyncio.create_task(self.start_poll())


	async def attempt_reconnect(self):
		log(f"[ConnectedDevice] Attempting to reconnect to device {self.name} at address {self.address}")
		new = await self.attempt_connect()	
		while new is None:
			log(f"[ConnectedDevice] Failed to reconnect to device {self.name} at address {self.address}, trying again in {RETRY_RATE} seconds")
			await asyncio.sleep(RETRY_RATE)
			new = await self.attempt_connect()
		self = new

	
	async def start_poll(self):
		try:
			while self.connection:
				await asyncio.sleep(POLL_RATE)
				self.mailbox.update(self.poll(), self.contactbook)
		except Exception as e:
			log(f"[ConnectedDevice::start_poll] {e}")
			self.connection = False
			await self.attempt_reconnect()
	
	#private
	@staticmethod
	def init__pbap(address:str):
		try:
			if not os.path.exists(ConnectedDevice.__pbap_dir):
				os.mkdir(ConnectedDevice.__pbap_dir)
			file_path	= ConnectedDevice.__pbap_dir + f"phonebook_{address.replace(":", "_")}.vcf"
			if not os.path.exists(file_path):
				log("[ConnectedDevice] Creating phonebook file")
				createPBAPSession(address)(file_path, {})
				if os.path.exists(file_path):
					log("[ConnectedDevice::init__pbap] Success!")
			return True
		except Exception as e:
			if isinstance(e, PermissionError):
				log("[ConnectedDevice::init__pbap] Failed! - Please create /opt/pybt/ directory and try again (make sure you have write permissions)")
			else:
				log(f"[ConnectedDevice::init__pbap] Failed! - {e}")
			return False

	def update_mailbox(self, obex_msg: dict):
		self.mailbox.update(obex_msg, self.contactbook)
		pass

