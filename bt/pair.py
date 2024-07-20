import dbus
import dbus.proxies
from .err import DeviceUnreachableError

sysbus = dbus.SystemBus()


def get_device_name(mac_address:str) -> str:
	try:
		proxy = sysbus.get_object("org.bluez", "/org/bluez/hci0/dev_" + mac_address.replace(":", "_"))
		props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
		return props.Get("org.bluez.Device1", "Name")
	except dbus.exceptions.DBusException as e:
		raise DeviceUnreachableError("Device not found", "get_device_name")


def pair(mac_address:str) -> bool:
	#pair device
	adapter = sysbus.get_object("org.bluez", "/org/bluez/hci0")
	adapter_if = dbus.Interface(adapter, "org.bluez.Adapter1")
	adapter_if.StartDiscovery()
	adapter_if.PairDevice(mac_address)
	adapter_if.ConnectDevice(mac_address)
	return True 

def start_discovery() -> None:
	adapter = sysbus.get_object("org.bluez", "/org/bluez/hci0")
	adapter_if = dbus.Interface(adapter, "org.bluez.Adapter1")
	adapter_if.StartDiscovery()

def stop_discovery() -> None:
	adapter = sysbus.get_object("org.bluez", "/org/bluez/hci0")
	adapter_if = dbus.Interface(adapter, "org.bluez.Adapter1")
	adapter_if.StopDiscovery()

"""
dev: Device | str
"""
def isConnected(dev : str) -> bool:
	#check if device is connected
	address = dev
	proxy = sysbus.get_object(
		"org.bluez",
		"/org/bluez/hci0/dev_" + address.replace(":", "_")
	)
	props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
	connected = props.Get("org.bluez.Device1", "Connected")
	if connected == 'false':
		return False
	else:
		return True

def connect(mac_address:str) -> bool:
	try:
		if isConnected(mac_address):
			return True
		else:
			adapter = sysbus.get_object("org.bluez", "/org/bluez/hci0/dev_" + mac_address.replace(":", "_")) 
			adapter_if = dbus.Interface(adapter, "org.bluez.Network1")
			adapter_if.Connect(mac_address)
			return isConnected(mac_address)
	except dbus.exceptions.DBusException as e:
		raise DeviceUnreachableError("Device not found", "connect")
		return False;
		
