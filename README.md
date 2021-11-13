# Helm Deck

A dashboard/controller for a boat.

Show some simple status and have buttons control aspects of the ship via
REST calls and/or NMEA2000 packets. Also has a webserver to receive API
calls.

This is currently a work in progress and should not be used for anything
except example code and maybe not even for that.

## Docs

* https://python-elgato-streamdeck.readthedocs.io/en/stable/index.html
* https://github.com/abcminiuser/python-elgato-streamdeck
* https://github.com/kneufeld/streamdeckui

If you're looking for example code for `streamdeckui` see [helmdeck/helmdeck.py](helmdeck/helmdeck.py)

## Installation

```
pip install -e .
```

See [this](https://python-elgato-streamdeck.readthedocs.io/en/stable/pages/installation.html)
for more info regarding getting `streamdeck` working.


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
