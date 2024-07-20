import threading
import os
from datetime import datetime as Date
from model.mailbox import Mailbox
from bt.pbap import createPBAPSession
from bt.map import createMAPSession



if not os.path.exists("/tmp"):
	os.mkdir("/tmp")

if not os.path.exists("/tmp/phonebook.vcf"):
	print("Creating phonebook file")
	createPBAPSession()("/tmp/phonebook.vcf", {})
	
msg = createMAPSession()
msgs = msg("", {})
mailbox = Mailbox.from_obex(msgs)
print(mailbox.to_string())

while True:
	#sleep thread
	threading.Event().wait(1)
	msgs = msg("", {})
	mailbox.update(msgs)
	print("NEW LINE BEEBS!")
	print(mailbox.to_string())


