import dbus
import dbus.proxies
from util.log import error

class BusError(Exception):
	def __init__(self, message, source):
		self.message = f"[{source}]:{message}" 
	pass

class ObexError(BusError):
	def __init__(self, message, source):
		super().__init__(message, source)
		pass

class DeviceUnreachableError(BusError):
	def __init__(self, message, source):
		super().__init__(message, source)
		pass 

class DeviceDisconnectedError(BusError):
	def __init__(self, source):
		super().__init__("Device Disconnected", source)
		pass

def obex_error(err : dbus.exceptions.DBusException, session : dbus.proxies.ProxyObject) -> None:
	if err.get_dbus_name() == "org.bluez.obex.Error.Failed":
		error(f"General Failure: {err.get_dbus_message()}")
	elif err.get_dbus_name() == "org.bluez.obex.Error.InvalidArguments":
		error("Invalid Arguments")
	else:
		error(f"Error: {err.get_dbus_name()}")
		error(f"Message: {err.get_dbus_message()}")
	#close session
