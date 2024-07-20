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

