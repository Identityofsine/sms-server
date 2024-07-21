import dbus
import dbus.proxies
import asyncio
from typing import Callable

from model.contact import Contact
from model.contactbook import ContactBook
from .message import Message
from util.log import log

class Mailbox:
	messages: list[Message] 
	src: str = "Mailbox"

	def __init__(self, messages):
		self.messages = messages

	@staticmethod
	def from_obex(obex_msg: dbus.Dictionary, contactbook: ContactBook | None):
		try:
			messages = []
			for key in obex_msg.keys():
				msg = obex_msg[key]
				sender = None
				if contactbook is not None:
					sender = contactbook.get_contact(msg["Sender"])
				if sender is None:
					sender = Contact(msg["Sender"], msg["Sender"], msg["Sender"]) 

				msg_obj = Message(sender, msg["Subject"], msg["Timestamp"], f"{key}", True if msg["Read"] == 1 else False)
				messages.append(msg_obj)
			log(f"[{Mailbox.src}] Created mailbox with {len(messages)} messages")
			return Mailbox(messages)
		except Exception as e:
			log(f"[{Mailbox.src}] {e}")
			return None

	def update(self, obex_msg: dbus.Dictionary, contactbook: ContactBook | None):
		if obex_msg is None:
			log (f"[{Mailbox.src}] No messages to update")
			return
		log(f"[{Mailbox.src}] Updating mailbox with {len(obex_msg)} messages")
		for key in obex_msg.keys():
			i = self.get_message(key)
			msg = obex_msg[key]
			sender = None
			if i is not None:
				i.read = True if obex_msg[key]["Read"] == 1 else False	
				# see if we can get the contact from the contactbook
				if i.sender.name == msg["Sender"] and contactbook is not None:
					sender = contactbook.get_contact(msg["Sender"])
					if sender is not None:
						i.sender = sender
				continue
			else :
				if contactbook is not None:	
					log(f"[{Mailbox.src}] Attempting to get contact {msg['Sender']} from contactbook")
					sender = contactbook.get_contact(msg["Sender"])
				if sender is None:
					sender = Contact(msg["Sender"], msg["Sender"], msg["Sender"])
				msg_obj = Message(sender, msg["Subject"], msg["Timestamp"], key, True if msg["Read"] == 1 else False)
				self.messages.append(msg_obj)
		self.sort()
		pass	

	def sort(self):
		#reverse sort by date
		self.messages.sort(key = lambda x: x.date, reverse = True)

	def get_message(self, key: str):
		for msg in self.messages:
			if msg.path == key:
				return msg
		return None


	def to_string(self):
		return "\n\n".join([msg.to_string() for msg in self.messages])
		#return self.messages[0].to_string() 

	def to_json(self):
		return [self.messages[i].to_json() for i in range(len(self.messages))]



