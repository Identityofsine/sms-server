from typing_extensions import Buffer


class Contact():
	uid: str
	name: str
	number: str
	photo: str 

	def __init__(self, uid: str, name: str, number: str, photo: str = ""):
		self.uid = str(uid)
		self.name = str(name)
		self.number = str(number).replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
		self.photo = str(photo)

	def to_dict(self):
		return {"uid": self.uid, "name": self.name, "number": self.number, "photo": self.photo}

	def to_string(self):
		return f"UID: {self.uid}\nName: {self.name}\nNumber: {self.number}\nPhoto: {self.photo}"


