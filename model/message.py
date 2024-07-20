import dbus
import dbus.proxies
from datetime import datetime as Date
from util.dateparse import convert_to_datetime

class Message:
	path: str
	sender: str
	subject: str
	date: Date
	read: bool

	def __init__(self, sender : str, subject: str, date : str, path = "", read = False):
		self.sender = sender
		self.subject = subject
		self.date = convert_to_datetime(date) 
		self.path = path
		self.read = False

	def to_string(self):
		return f"From: {self.sender}\nSubject: {self.subject}\nDate: {self.date}\nRead: {self.read}"


