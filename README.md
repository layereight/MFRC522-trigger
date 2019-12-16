# MFRC522-trigger

* trigger arbitrary action when the MFRC522 detects an NFC tag
* supported actions are
  * curling a URL
  * executing a command line
* based on [pirc522](https://github.com/ondryaso/pi-rc522) which is based on the famous 
[MFRC522-python](https://github.com/mxgxw/MFRC522-python)

# Prerequisites

* ssh into your Raspberry Pi and execute
```
$ sudo apt-get update
$ sudo apt-get install python-dev python-pip vim
$ sudo pip install RPi.GPIO
$ sudo pip install spidev
$ sudo pip install pi-rc522
```
* edit Raspberry Pi's */boot/config.txt*: `$ sudo vi /boot/config.txt`
* add the following lines somewhere in the file
```
dtparam=spi=on
dtoverlay=pi3-disable-bt
enable_uart=1
```
* reboot: `sudo reboot`

# Configuration

## JSON schema

```json
{
  "type": "object",
  "patternProperties": {
    "^[0-9]+$": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "title": "Alias name for the tag with the given id."
        },
        "url": {
          "type": "string",
          "title": "Default action. Url to curl when the tag is detected."
        },
        "onremove": {
          "type": "string",
          "title": "Optional action. Url to curl when the tag is removed."
        },
        "onredetect": {
          "type": "string",
          "title": "Optional action. Url to curl when the tag is re-detected after it was removed."
        }
      },
      "required": ["name", "url"]
    }
  }
}
```

## Example configuration

```json
{
  "1234567890123": {
    "name": "A very nice tag",
    "url": "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=my_playlist_1"
  },
  "9876543210987": {
    "name": "An even nicer tag",
    "url": "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=my_playlist_2",
    "onremove": "http://localhost:3000/api/v1/commands/?cmd=pause",
    "onredetect": "http://localhost:3000/api/v1/commands/?cmd=play"
  },
  "5432109876543": {
    "name": "This tag is also nice",
    "url": "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=my_playlist_3"
  }
}
```

# Roadmap

* document Ansible playbook
* Ansible playbook: set volumio logging level to error to reduce cpu load on Raspberry Pi Zero
* document logging.ini
* play beep sound when rfid tag is detected

# Roadmap done

* command actions: execute a system command as action
* migrate to python3
* toggle actions: execute the same action when a rfid tag is removed from the reader and re-detected
* action on tag remove event
* action on tag re-detected event
* document config.json

# Inspiration

* https://github.com/MiczFlor/RPi-Jukebox-RFID
* https://github.com/MiczFlor/RPi-Jukebox-RFID/issues/5

# Links

* https://github.com/ondryaso/pi-rc522
* http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio
* https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi
* https://howchoo.com/g/ytzjyzy4m2e/build-a-simple-raspberry-pi-led-power-status-indicator
* https://github.com/MiczFlor/RPi-Jukebox-RFID/blob/master/scripts/installscripts/stretch-install-default.sh#L468
* https://volumio.org/forum/245-does-not-boot-with-enable-uart-t7194.html
* http://blog.mmone.de/2017/05/16/raspberry-pi-zero-w-disable-bluetooth/
* https://github.com/miguelbalboa/rfid
* http://praktische-elektronik.dr-k.de/Praktikum/Analog/Le-LED-Schaltungen.html
