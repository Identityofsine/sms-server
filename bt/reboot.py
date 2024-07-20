from os import system
from util.log import log
import asyncio

async def reboot_service(service: str, user_session: bool = False):

	log(f"[reboot_service]Restarting {service}")
	if user_session:
		system(f"systemctl --user restart {service}")
	else:
		system(f"systemctl restart {service}")
	pass

async def reboot_bluetooth():
	await reboot_service("bluetooth")
	pass

async def reboot_obex():
	await reboot_service("obex", True)
	pass

