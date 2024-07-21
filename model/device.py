from .mailbox import Mailbox
import threading
import os
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
				mb = Mailbox.from_obex(msgs, msg)
				while mb is None:
					log(f"[{self.src}] Failed to connect to device {self.name} at address {self.address}, trying again in 2 seconds")
					threading.Event().wait(2)
					mb = Mailbox.from_obex(msgs, msg)
				return ConnectedDevice(self.address, get_device_name(self.address), mb)
			else:
				log(f"[{self.src}] Failed to connect to device {self.name} at address {self.address}")
				return None
		except Exception as e:
			if mb is not None:
				mb.stoppolling()
			log(f"[{self.src}::attempt_connect] {e}")
			return None

class ConnectedDevice(Device):
	mailbox: Mailbox

	def __init__(self, address:str, name:str, mailbox:Mailbox):
		super().__init__(address, name)
		log(f"[ConnectedDevice] Connected to device {name} at address {address}")
		self.mailbox = mailbox
	
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

