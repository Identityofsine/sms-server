import dbus
import dbus.proxies
from typing import Callable
from .err import obex_error

session_bus = dbus.SessionBus()

def createMAPSession() -> Callable:
	obex = session_bus.get_object(
					'org.bluez.obex',
					'/org/bluez/obex',
	)
	obex_if = dbus.Interface(obex, 'org.bluez.obex.Client1')
	#dict with {"Target":"MAP"}
	#print methods
	try:
		session = obex_if.CreateSession("78:FB:D8:94:FC:68", {"Target":"MAP"})
		session_proxy = session_bus.get_object('org.bluez.obex', session)
		session_if = dbus.Interface(session_proxy, 'org.bluez.obex.MessageAccess1')
		SetFolder = session_if.SetFolder
		SetFolder("telecom/msg/inbox")
		ListFolders = session_if.ListFolders
		print(ListFolders({'Name':"telecom"}))
		ListMessages = session_if.ListMessages 
		return ListMessages
	except dbus.exceptions.DBusException as e:
		obex_error(e, obex)
		return lambda x, y: "Error" 


