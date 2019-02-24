# MFRC522-trigger

* trigger arbitrary action when the MFRC522 detects an NFC tag
* currently only supports curling a URL
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

# Roadmap

* document config.json
* Ansible playbook: install MFRC522-trigger via git clone, do all prerequisites
* document Ansible playbook
* document logging.ini
* play beep sound when rfid tag is detected
* toggle actions: execute the same action when a rfid tag is removed from the reader and re-detected
* command actions: execute a system command as action

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
