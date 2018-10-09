# MFRC522-trigger

* trigger arbitrary action when the MFRC522 detects an NFC tag
* currently only supports curling a URL
* based on [pirc522](https://github.com/ondryaso/pi-rc522) which is based on the famous 
[MFRC522-python](https://github.com/mxgxw/MFRC522-python)

# Prerequisites

```
$ sudo apt-get install python-pip
$ sudo pip install spidev
$ sudo pip install pi-rc522
```

*/boot/config.txt*
```
dtparam=spi=on
dtoverlay=pi3-disable-bt
enable_uart=1
```

# Inspiration

* https://github.com/MiczFlor/RPi-Jukebox-RFID

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
