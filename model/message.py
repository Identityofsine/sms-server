import dbus
import math
import random
import dbus.proxies
from datetime import datetime as Date
from util.dateparse import convert_to_datetime
from .contact import Contact

def random_uid_generator():
	return str(random.randint(0, 1000000))

class Message:
	id: str
	path: str
	sender: Contact
	subject: str
	date: Date
	read: bool

	def __init__(self, sender : Contact, subject: str, date : str, path = "", read = False):

		self.id = random_uid_generator() 
		self.sender = sender 
		self.subject = str(subject)
		self.date = convert_to_datetime(date) 
		self.path = str(path)
		self.read = read 

	def to_string(self):
		return f"From: {self.sender.name}\nSubject: {self.subject}\nDate: {self.date}\nRead: {self.read}"

	def to_json(self):
		#hour and days
		date = self.date.date().strftime("%m/%d/%Y") + " " + self.date.time().strftime("%H:%M:%S")
		return {"id": self.id, "sender": self.sender.to_dict(), "subject": self.subject, "date": date, "read": self.read}



