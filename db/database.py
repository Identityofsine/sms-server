import os
from typing_extensions import ReadOnly
from util.log import log
import json

#JSON Serialization
class DeviceInfo():
	name:str
	address:str
	last_connected:str

	def __init__(self, name:str, address:str):
		self.name = name
		self.address = address
		self.last_connected = "Never"

	@staticmethod
	def from_device(device):
		return DeviceInfo(device.name, device.address)


class Database(object):
	__path = f"{os.path.dirname(os.path.realpath(__file__))}/../data/"
	__devices_file = "devices.json"
	__devices = [] 
	__instance = None
	
	#private
	def __init__(self):
		#make sure only one instance is created
		if Database.__instance is not None:
			raise Exception("This class is a singleton!")
		else:
			log("[Database] Creating database instance")
			self.__load()
			Database.__instance = self
		pass

	@staticmethod
	def get_instance():
		if Database.__instance is None:
			Database.__instance = Database()
		return Database.__instance

	def __load(self):
		try:
			log(f"[Database] Loading database from {self.__path}")
			with open(self.__path + self.__devices_file, "r") as f:
				data = f.read()
				data = json.loads(data)
				self.__devices = data["devices"]
		except Exception as e:
			if isinstance(e, FileNotFoundError):
				log(f"[Database] No database found at {self.__path}... Creating One!")
				self.__devices = []
				self.__save()
			else: 
				log(f"[Database] Failed to load database: {e}")
		pass

	def __save(self):
		try:
			if not os.path.exists(self.__path):
				os.mkdir(self.__path)

			log(f"[Database] Saving database to {self.__path}")
			with open(self.__path + self.__devices_file, "w") as f:
				f.write(json.dumps({"devices":[obj.__dict__ for obj in self.__devices]}))
		except Exception as e:
			log(f"[Database] Failed to save database: {e}")
		pass

	def add_device(self, device:DeviceInfo):
		log(f"[Database] Adding device {device.name} at address {device.address}")
		for d in self.__devices:
			if d["address"] == device.address:
				d["name"] = device.name
				d["last_connected"] = device.last_connected
				self.__save()
				return
		self.__devices.append(device)
		self.__save()



	

