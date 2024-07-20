import dbus
import dbus.proxies
from typing import Callable
from .err import obex_error
from util.log import log

session_bus = dbus.SessionBus()

def createPBAPSession(address: str) -> Callable:
	log("[PBAP] Creating PBAP session")
	obex = session_bus.get_object(
					'org.bluez.obex',
					'/org/bluez/obex',
	)
	obex_if = dbus.Interface(obex, 'org.bluez.obex.Client1')
	#dict with {"Target":"PBAP"}
	try:
		session = obex_if.CreateSession(address, {"Target":"PBAP"})
		session_proxy = session_bus.get_object('org.bluez.obex', session)
		session_if = dbus.Interface(session_proxy, 'org.bluez.obex.PhonebookAccess1')
		Select = session_if.Select
		Select("int", "pb")
		PullAll = session_if.PullAll;
		return lambda x, y: PullAll(x, y); session_if.RemoveSession(session) 
	except dbus.exceptions.DBusException as e:
		obex_error(e, obex)
		return lambda: "Error"


