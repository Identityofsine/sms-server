import dbus
import dbus.proxies
from datetime import datetime as Date
from util.dateparse import convert_to_datetime
from .contact import Contact

class Message:
	path: str
	sender: Contact
	subject: str
	date: Date
	read: bool

	def __init__(self, sender : Contact, subject: str, date : str, path = "", read = False):
		self.sender = sender 
		self.subject = str(subject)
		self.date = convert_to_datetime(date) 
		self.path = str(path)
		self.read = False

	def to_string(self):
		return f"From: {self.sender.name}\nSubject: {self.subject}\nDate: {self.date}\nRead: {self.read}"

	def to_json(self):
		return {
			"sender" : self.sender.__dict__,
			"subject" : self.subject,
			"date" : str(self.date),
			"read" : self.read
		}


