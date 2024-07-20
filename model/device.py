from .mailbox import Mailbox
import threading
import os
from util.log import log
from bt.pbap import createPBAPSession
from bt.map import createMAPSession
from bt.pair import connect

class Device:
	address:str 
	name:str
	src:str = "Device"

	def __init__(self, address:str, name:str):
		self.address = address
		self.name = name
	
	async def attempt_connect(self): 
		#connect to device
		try:
			log(f"Attempting to connect to device {self.name} at address {self.address}")
			if connect(self.address):
				log(f"[{self.src}] Connected to device {self.name} at address {self.address}")
				msg = createMAPSession(self.address)
				log(f"[{self.src}] Connected to MAP session")
				msgs = msg()
				log(f"[{self.src}] Connected to OBEX session")
				mb = Mailbox.from_obex(msgs, msg)
				while mb is None:
					log(f"[{self.src}] Failed to connect to device {self.name} at address {self.address}, trying again in 2 seconds")
					threading.Event().wait(2)
					mb = Mailbox.from_obex(msgs, msg)
				return ConnectedDevice(self.address, self.name, mb)
			else:
				log(f"[{self.src}] Failed to connect to device {self.name} at address {self.address}")
				return None
		except Exception as e:
			log(f"[{self.src}] {e}")
			return None

class ConnectedDevice(Device):
	mailbox: Mailbox

	def __init__(self, address:str, name:str, mailbox:Mailbox):
		super().__init__(address, name)
		self.mailbox = mailbox
		self.__init__pbap()
	
	#private
	def __init__pbap(self):
		if not os.path.exists("/tmp"):
			os.mkdir("/tmp")
		if not os.path.exists("/tmp/phonebook.vcf"):
			log("Creating phonebook file")
			createPBAPSession()("/tmp/phonebook.vcf", {})
		pass

	def __init__map(self):
		pass

