import dbus
import dbus.proxies

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
		print(f"General Failure: {err.get_dbus_message()}")
	elif err.get_dbus_name() == "org.bluez.obex.Error.InvalidArguments":
		print("Invalid Arguments")
	else:
		print(f"Error: {err.get_dbus_name()}")
		print(f"Message: {err.get_dbus_message()}")
	#close session
