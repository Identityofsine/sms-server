import dbus
import dbus.proxies
from typing import Callable
from .err import obex_error

session_bus = dbus.SessionBus()

def createPBAPSession() -> Callable:
	obex = session_bus.get_object(
					'org.bluez.obex',
					'/org/bluez/obex',
	)
	obex_if = dbus.Interface(obex, 'org.bluez.obex.Client1')
	#dict with {"Target":"PBAP"}
	try:
		session = obex_if.CreateSession("78:FB:D8:94:FC:68", {"Target":"PBAP"})
		session_proxy = session_bus.get_object('org.bluez.obex', session)
		session_if = dbus.Interface(session_proxy, 'org.bluez.obex.PhonebookAccess1')
		Select = session_if.Select
		Select("int", "pb")
		PullAll = session_if.PullAll
		return PullAll
	except dbus.exceptions.DBusException as e:
		obex_error(e, obex)
		return lambda x, y: "Error"


