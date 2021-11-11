# Wave Deck (name is a work in progress)

A dashboard/controller for a boat.

Show some simple status and have buttons control aspects of the ship via
REST calls and/or NMEA2000 packets. Also has a webserver to receive API
calls.

## Potential better names

* RiverDash
* BrookHull
* HelmDeck
* HelmsDeep
* Helminator (not really)

## Docs

* https://python-elgato-streamdeck.readthedocs.io/en/stable/index.html
* https://github.com/abcminiuser/python-elgato-streamdeck


## Installation

See [this](https://python-elgato-streamdeck.readthedocs.io/en/stable/pages/installation.html)
but the _tl;dr_ is...

### OSX

```bash
brew install hidapi
```

### Linux

```bash
# system packages needed for the default LibUSB HIDAPI backend
apt install -y libudev-dev libusb-1.0-0-dev libhidapi-libusb0

# system packages needed for the Python Pillow package installation
apt install -y libjpeg-dev zlib1g-dev libopenjp2-7 libtiff5

# some udev shinanigans...
```

## Goals

* show status: battery level, depth, wind, time
* show alerts. Same as status with a different colour?
* control: turn on lights/stereo/anchor alarm/etc (via relays, nmea msgs, rest, etc)
* maybe control touchscreen? Thinking the victron raspberry pi app thing, put in foreground?

## Design

* webserver
    * receive prometheus alerts
    * receive nmea2000 messages (via some other software)
* ui framework
    * need to easily make pages, buttons, etc
