<a href="https://github.com/layereight/MFRC522-trigger/actions">
  <img alt="GitHub Actions status" src="https://github.com/layereight/MFRC522-trigger/workflows/test/badge.svg" />
</a>

# MFRC522-trigger

* trigger arbitrary action when the MFRC522 detects an NFC tag
* the MFRC522 is connected to a Raspberry Pi, for the wiring see [pirc522](https://github.com/ondryaso/pi-rc522#connecting)
* supported actions are
  * curling a URL
  * executing a command line
* based on [pirc522](https://github.com/ondryaso/pi-rc522) which is based on the famous 
[MFRC522-python](https://github.com/mxgxw/MFRC522-python)

# Prerequisites

* python3
* python modules RPi.GPIO, spidev, pi-rc522, assertpy
* enable the [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) on the Raspberry Pi using `raspi-config`

# Manual Installation

* ssh into your Raspberry Pi and execute
```
$ sudo apt-get update
$ sudo apt-get install python3 python3-pip vim
$ git clone https://github.com/layereight/MFRC522-trigger.git
$ sudo pip3 install -r MFRC522-trigger/requirements.txt
```
* edit Raspberry Pi's */boot/config.txt*: `$ sudo vi /boot/config.txt`
* add the following lines somewhere in the file
```
dtparam=spi=on
dtoverlay=pi3-disable-bt
enable_uart=1
```
* reboot: `sudo reboot`
* configure MFRC522-trigger config file `MFRC522-trigger/config.json`
* run `MFRC522-trigger/MFRC522-trigger.py`

# Automated Installation

* all the steps from the manual installation can be done automatically
* automated installation is achieved using [Ansible](https://docs.ansible.com/ansible/latest/index.html)
* Ansible is an automation tool, if you wanna know more about it have a look at 
  https://docs.ansible.com/ansible/latest/index.html
* install Ansible on your local machine https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
* on your local machine clone the repo https://github.com/layereight/MFRC522-trigger
```
$ git clone https://github.com/layereight/MFRC522-trigger.git
$ cd MFRC522-trigger/ansible
$ vi inventory
```
* replace the contents of the file *inventory* to point to your music box (e.g. my_raspi_host)
```
[my_pi]
my_raspi_host ansible_host=192.168.1.100 ansible_user=pi ansible_ssh_pass=raspberry
```
* execute the ansible playbook, it runs for roughly 10 minutes, so go grab a coffee ;-)
```
$ ansible-playbook -i inventory MFRC522-trigger.yml 

PLAY [Install prerequisite software] ************************************************

TASK [Install prerequisite debian packages] *****************************************
changed: [my_raspi_host]

TASK [Install pip requirements file] ************************************************
changed: [my_raspi_host]

TASK [Install prerequisite pip packages] ********************************************
changed: [my_raspi_host]

PLAY [Prepare Raspberry Pi's /boot/config.txt] **************************************

TASK [Alter /boot/config.txt] *******************************************************
changed: [my_raspi_host]

TASK [Reboot the machine when /boot/config.txt was changed] *************************
changed: [my_raspi_host]

PLAY [Clone MFRC522-trigger from github] ********************************************

TASK [Create devel directory] *******************************************************
changed: [my_raspi_host]

TASK [Clone MFRC522-trigger from github] ********************************************
changed: [my_raspi_host]

TASK [Copy config.json from sample file] ********************************************
changed: [my_raspi_host]

PLAY [Install MFRC522-trigger as systemd service] ***********************************

TASK [systemd : Copy custom systemd service file] ***********************************
changed: [my_raspi_host]

TASK [systemd : Enable custom systemd service] **************************************
changed: [my_raspi_host]

TASK [systemd : Copy custom systemd service file] ***********************************
changed: [my_raspi_host]

TASK [systemd : Enable custom systemd service] **************************************
changed: [my_raspi_host]

TASK [systemd : Copy custom systemd service file] ***********************************
skipping: [my_raspi_host]

TASK [systemd : Enable custom systemd service] **************************************
skipping: [my_raspi_host]

PLAY RECAP **************************************************************************
my_raspi_host : ok=11 changed=11 unreachable=0 failed=0 skipped=2 rescued=0 ignored=0

```

# Configuration

## JSON schema

<!-- embedme config/config.schema.json -->

```json
{
  "definitions": {
    "actions": {
      "type": "array",
      "title": "Actions to trigger when the tag with the given id is detected for the given event.",
      "items": {
        "oneOf": [
          {
            "type": "object",
            "title": "Curl action",
            "required": ["type", "url"],
            "additionalProperties": false,
            "properties": {
              "type": {
                "type": "string",
                "title": "Type of action. Must be 'curl'.",
                "pattern": "^curl$"
              },
              "url": {
                "type": "string",
                "title": "Url to curl when the tag is detected.",
                "format": "uri"
              }
            }
          },
          {
            "type": "object",
            "title": "Command line action",
            "required": ["type", "command"],
            "additionalProperties": false,
            "properties": {
              "type": {
                "type": "string",
                "title": "Type of action. Must be 'command'.",
                "pattern": "^command$"
              },
              "command": {
                "type": "string",
                "title": "Command to execute when the tag is detected."
              }
            }
          }
        ]
      }
    }
  },

  "type": "object",
  "title": "The root schema",
  "additionalProperties": false,
  "patternProperties": {
    "^[0-9A-F:]+$": {
      "type": "object",
      "title": "Schema holding name and actions for a tag",
      "required": ["name", "ondetect"],
      "additionalProperties": false,
      "properties": {
        "name": {
          "type": "string",
          "title": "Alias name for the tag with the given id."
        },
        "ondetect": { "$ref": "#/definitions/actions" },
        "onremove": { "$ref": "#/definitions/actions" },
        "onredetect": { "$ref": "#/definitions/actions" }
      }
    }
  }
}

```

## Example configuration

<!-- embedme config.sample.json -->

```json
{
  "01:23:AB:CD": {
    "name": "A very nice 4-byte NUID tag, triggering 2 actions: playing a playlist and setting the volume.",
    "ondetect": [
      {
        "type": "curl",
        "url": "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=my_playlist_1"
      },
      {
        "type": "curl",
        "url": "http://localhost:3000/api/v1/commands/?cmd=volume&volume=40"
      }
    ]
  },
  "01:23:45:67:89:0A:BC": {
    "name": "An even nicer 7-byte UID tag",
    "ondetect": [
      {
        "type": "curl",
        "url": "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=my_playlist_2"
      }
    ],
    "onremove": [
      {
        "type": "curl",
        "url": "http://localhost:3000/api/v1/commands/?cmd=pause"
      }
    ],
    "onredetect": [
      {
        "type": "curl",
        "url": "http://localhost:3000/api/v1/commands/?cmd=play"
      }
    ]
  },
  "AA:BB:CC:DD:EE:FF:01": {
    "name": "This tag is also nice",
    "ondetect": [
      {
        "type": "command",
        "command": "sudo shutdown -h now"
      }
    ]
  }
}

```

# Version 2 Breaking Changes

Version 2.x of this software respects single (4 bytes) and double (7 bytes) sized UIDs as defined by ISO standard 14443-3.
Version 1.x was always assuming single sized UIDs and simply concatenated decimal string representations of each byte 
(e.g. `1364182229223`). Version 2.x assumes hexadecimal representation of each byte separated by a colon
(e.g. 4-byte `01:23:AB:CD`, e.g. 7-byte `01:23:45:67:89:0A:BC`).

This incompatability makes config files from version 1.x unusable with version 2.x. For easier config migration a tool
called `id-convert.py` is provided.

## Config Tag ID Migration Steps

* start `id-convert.py` and rescan all your tags, a file `ids.csv` is written containing a list of old style and new style tag ids
  ```
  $ ./id-convert.py | tee ids.csv
  ```
* backup your current config
  ```
  $ cp config.json config.json.bak
  ```
* replace old tag ids with new tag ids in your config file `config.json`
  ```
  $ for i in $(cat ids.csv); old=$(echo $i | cut -d '_' -f 1) && new=$(echo $i | cut -d '_' -f 2) && echo "${old} ${new}" && sed -i "s/${old}/${new}/g" config.json; done
  ```

# Roadmap

* more python unit tests
* Ansible playbook: set volumio logging level to error to reduce cpu load on Raspberry Pi Zero
* document logging.ini
* play beep sound when rfid tag is detected
* OTA updates

# Roadmap done

* ISO 14443 Tag IDs
* quit with error when config is broken
* validate config with JSON schema and log a warning when it's invalid
* multiple actions per event
* python unit tests
* githup actions ci
* document Ansible playbook
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
