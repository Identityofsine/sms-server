import dbus
import dbus.proxies

def obex_error(err : dbus.exceptions.DBusException, session : dbus.proxies.ProxyObject) -> None:
	if err.get_dbus_name() == "org.bluez.obex.Error.Failed":
		print(f"General Failure: {err.get_dbus_message()}")
	elif err.get_dbus_name() == "org.bluez.obex.Error.InvalidArguments":
		print("Invalid Arguments")
	else:
		print(f"Error: {err.get_dbus_name()}")
		print(f"Message: {err.get_dbus_message()}")
	#close session
