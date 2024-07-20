import dbus
import dbus.proxies
import asyncio
from typing import Callable
from .message import Message
from util.log import log

class Mailbox:
	messages: list[Message]
	poll: Callable 
	src: str = "Mailbox"

	def __init__(self, messages, poll):
		self.messages = messages
		self.poll = poll
		self.startpolling()
		

	def startpolling(self):
		asyncio.run(self.pollfunc())
	
	async def pollfunc(self):
		while True:
			await asyncio.sleep(5)
			try:
				self.update(self.poll())
			except Exception as e:
				log(f"[{Mailbox.src}] {e}")
				return

	@staticmethod
	def from_obex(obex_msg: dbus.Dictionary, poll: Callable):
		try:
			messages = []
			for key in obex_msg.keys():
				msg = obex_msg[key]
				msg_obj = Message(msg["Sender"], msg["Subject"], msg["Timestamp"], key, True if msg["Read"] == 1 else False)
				messages.append(msg_obj)
			log(f"[{Mailbox.src}] Created mailbox with {len(messages)} messages")
			return Mailbox(messages, poll)
		except Exception as e:
			return None

	def update(self, obex_msg: dbus.Dictionary):
		if obex_msg is None:
			log (f"[{Mailbox.src}] No messages to update")
			return
		log(f"[{Mailbox.src}] Updating mailbox with {len(obex_msg)} messages")
		for key in obex_msg.keys():
			i = self.get_message(key)
			if i is not None:
				i.read = True if obex_msg[key]["Read"] == 1 else False	
				continue
			else :
				msg = obex_msg[key]
				msg_obj = Message(msg["Sender"], msg["Subject"], msg["Timestamp"], key, True if msg["Read"] == 1 else False)
				self.messages.append(msg_obj)
		pass	

	def sort(self):
		#reverse sort by date
		self.messages.sort(key = lambda x: x.date, reverse = False)

	def get_message(self, key: str):
		for msg in self.messages:
			if msg.path == key:
				return msg
		return None


	def to_string(self):
		return "\n\n".join([msg.to_string() for msg in self.messages])

	def to_json(self):
		return [msg.__dict__ for msg in self.messages]



