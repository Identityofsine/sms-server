from typing_extensions import Buffer
import json
import base64

class Contact():
	uid: str
	name: str
	number: str
	photo: str 

	def __init__(self, uid: str, name: str, number: str, photo: str = ""):
		self.uid = str(uid)
		self.name = str(name)
		self.number = str(number).replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
		self.photo = photo

	def to_dict(self):
		return {"uid": self.uid, "name": self.name, "number": self.number, "photo": f"data:image/png;base64,{str(self.photo)}" if self.photo is not None and self.photo != "" else ''}

	def to_string(self):
		return f"UID: {self.uid}\nName: {self.name}\nNumber: {self.number}\nPhoto: {self.photo}"

	def to_json(self):
		return json.dumps(self.to_dict())


