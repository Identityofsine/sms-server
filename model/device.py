from .mailbox import Mailbox

class Device:
	address:str 
	name:str
	def __init__(self, address:str, name:str):
		self.address = address
		self.name = name
	
	def attempt_connect(self): 
		mailbox = Mailbox.from_obex({})
		return ConnectedDevice(self.address, self.name, mailbox)

class ConnectedDevice(Device):
	mailbox: Mailbox

	def __init__(self, address:str, name:str, mailbox:Mailbox):
		super().__init__(address, name)
		self.mailbox = mailbox
		self.__init__pbap()
	
	#private
	def __init__pbap(self):
		pass

