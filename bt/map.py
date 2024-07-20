import dbus
import dbus.proxies
from typing import Callable
from .err import obex_error, DeviceDisconnectedError
from .pair import isConnected

session_bus = dbus.SessionBus()

def createMAPSession(mac: str) -> Callable:
	obex = session_bus.get_object(
					'org.bluez.obex',
					'/org/bluez/obex',
	)
	obex_if = dbus.Interface(obex, 'org.bluez.obex.Client1')
	#dict with {"Target":"MAP"}
	#print methods
	session_outside = None
	try:
		session = obex_if.CreateSession(mac, {"Target":"MAP"})
		session_outside = session
		session_proxy = session_bus.get_object('org.bluez.obex', session)
		session_if = dbus.Interface(session_proxy, 'org.bluez.obex.MessageAccess1')
		SetFolder = session_if.SetFolder
		SetFolder("telecom/msg/inbox")
		ListFolders = session_if.ListFolders
		ListMessages = session_if.ListMessages 
		def get_messages():
			try: 
				if isConnected("78:FB:D8:94:FC:68"):
					messages = ListMessages("", {})
					return messages
				else: 
					raise DeviceDisconnectedError("createMAPSession") 
			except dbus.exceptions.DBusException as e:
				obex_error(e, obex)
				if session_outside is not None:
					obex_if.CloseSession(session_outside)
				raise DeviceDisconnectedError("createMAPSession")
		return get_messages
	except dbus.exceptions.DBusException as e:
		obex_error(e, obex)
		raise DeviceDisconnectedError("createMAPSession")



