import dbus
import dbus.proxies
from .message import Message

class Mailbox:
	messages: list[Message]

	def __init__(self, messages):
		self.messages = messages
	
	@staticmethod
	def from_obex(obex_msg: dbus.Dictionary):
		messages = []
		for key in obex_msg.keys():
			msg = obex_msg[key]
			msg_obj = Message(msg["Sender"], msg["Subject"], msg["Timestamp"], key, True if msg["Read"] == 1 else False)
			messages.append(msg_obj)
		return Mailbox(messages)

	def update(self, obex_msg: dbus.Dictionary):
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
		self.messages = sorted(self.messages, key = lambda x: x.date)

	def get_message(self, key: str):
		for msg in self.messages:
			if msg.path == key:
				return msg
		return None


	def to_string(self):
		return "\n\n".join([msg.to_string() for msg in self.messages])



