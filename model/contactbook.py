from .contact import Contact
import vobject
import base64
from util.log import log

class ContactBook():
	contacts: list[Contact]

	def __init__(self, dict: list[Contact]):
		self.contacts = dict
		pass

	@staticmethod
	def from_vcard(path : str):
		try: 
			contacts = []
			with open(path, "r") as f:
				for vcard in vobject.base.readComponents(f):
					contact = vcard.contents
					#ignore errors
					uid = str(contact['uid'][0].transformToNative().value)
					name = str(contact['fn'][0].transformToNative().value)
					number = str(contact['tel'][0].transformToNative().value).replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
					try:
						photo = base64.b64encode(contact['photo'][0].transformToNative().value).decode("utf-8")
					except KeyError:
						photo = ""
					contacts.append(Contact(uid, name, number, photo))

			return ContactBook(contacts)
		except Exception as e:
			log(f"[ContactBook::from_vcard] {e}")
			return None
	
	def get_contact(self, number: str):
		for c in self.contacts:
			if c.number == number.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", ""):
				return c
		return None
