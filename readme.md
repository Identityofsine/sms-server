# BT-SMS Server 

This is a simple *stdout* server that listens for incoming SMS messages and prints them out in a JSON format. This is powered using Bluetooth, python-dbus and BlueZ. 

This project will prove very useful for those who want to interface their phone's SMS messages with their computer. This is project is also designed to be run on a Raspberry Pi or any other Linux-based system -- allowing you to have a dedicated SMS receiver. This is perfect for intergrating with IoT projects such as one of those smart mirrors or a home automation system.

## Features
- [x] Read incoming SMS messages
- [x] Read incoming MMS messages

## Note

This is currently a work in progress and in result is not fully stable. But it is designed to be a simple and easy way to interface your phone's texts with your computer using the MAP profile.

## Requirements
- Python 3
- Linux-based OS
- BlueZ
- BlueZ Obex Library
- Bluetooth Adapter

## Installation

### Pre-requisites

**1. Install the Bluez and Bluez Obex Library**

#### Debian-based systems
```bash
sudo apt-get install bluez bluez-obexd
```

#### Arch-based systems
```bash
sudo pacman -S bluez bluez-utils
#using yay
yay -S bluez-obex
```

**2. Enable the Bluetooth services**

> Personally, I had a really hard time getting the Bluetooth services to work...

```bash
sudo systemctl enable bluetooth #works
sudo systemctl start bluetooth #works

#might not work
sudo systemctl enable obex 
sudo systemctl start obex
```

> If you have an error with the obex service, try to enable and start the service in the user session
```bash
systemctl --user enable obex
systemctl --user start obex
```

**3. Pair your phone using `bluetoothctl`**

### Project Installation 

> Run:
```bash
git clone https://github.com/Identityofsine/sms-server && cd sms-server && pip install -r requirements.txt 
```

## Usage

After you have paired your phone with your computer, you can run the server using the following command:

```bash
python __init__.py --device <device_address>
```

> Find the `<device_address>` using the `bluetoothctl` command

By default, the server will print out the incoming messages in a redundant JSON format. 

```json
{
    "sender": "+18885521442",
    "subject": "their message",
    "timestamp": "2024-07-01 12:00:00"
}
```

> You can also enable a more human readable format by adding the `--pretty` or `-p` flag

```bash
python __init__.py --device <device_address> --pretty
```

### Verbose

You can also run the server in verbose mode by adding the `--debug` flag

```bash
python __init__.py --device <device_address> --debug
```

## The Future

> Note: PBAP support is here, I just haven't had the time to implement reading vcards yet.

I plan to add more features to this project such as the ability to send messages, read contacts, send commands through stdio, and more.

Most importantly, I plan to dockerize this project and make it much more easy to setup and use.

## Links

- [BlueZ](https://git.kernel.org/pub/scm/bluetooth/bluez.git/)
- [BlueZ Obex](https://git.kernel.org/pub/scm/bluetooth/obexd.git/)
- [BlueZ Documentation](https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc)
- [BlueZ Obex Documentation](https://git.kernel.org/pub/scm/bluetooth/obexd.git/tree/doc)
- [Bluetooth](https://www.bluetooth.com/)
- [Bluetooth SIG](https://www.bluetooth.com/specifications/specs/)
- [Bluetooth SIG MAP](https://www.bluetooth.com/specifications/profiles-overview/)
- [Bluetooth SIG MAP Spec](https://www.bluetooth.com/specifications/profiles-overview/)

### Links that I need to read
- [StackOverflow: Docker Bluetooth Passthrough](https://stackoverflow.com/questions/28868393/accessing-bluetooth-dongle-from-inside-docker)


