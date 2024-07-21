# BT-SMS Server 

This is a simple *stdout* server that listens for incoming SMS messages and prints them out in a JSON format. This is powered using Bluetooth, python-dbus and BlueZ. 

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
