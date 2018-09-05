#!/usr/bin/python

import RPi.GPIO as GPIO
import MFRC522
import signal
# import urllib.request
import urllib2

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

map = {
    '2081011237143': {
        'id': 2081011237143,
        'name': 'Checkcard',
        'url': 'http://localhost:3000/api/v1/commands/?cmd=stop'
    },
    '13648060224': {
        'id': 13648060224,
        'name': 'Buddha',
        'url': 'http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=Traumzauberbaum'
    },
    '25324884211130': {
        'id': 25324884211130,
        'name': "Blue Tag",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=Kinderlieder"
    },
    '12344': {
        'id': 12344,
        'name': "Mobile Phone",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    },
    '13648823361': {
        'id': 13648823361,
        'name': "Loewe",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    },
    '13647223446': {
        'id': 13647223446,
        'name': "Zebra",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    },
    '1364223226177': {
        'id': 1364223226177,
        'name': "Giraffe",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    },
    '1364209227190': {
        'id': 1364209227190,
        'name': "Hyaene",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    },
    '1364215226185': {
        'id': 1364215226185,
        'name': "Elefant",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    },
    '13648223553': {
        'id': 13648223553,
        'name': "Nilpferd",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    }
}

def execute_id(tag_id):
    if (tag_id not in map):
        print("No mapping for tag " + tag_id)
        return
    # print("CARD_ID " + card_id)
    card = map[tag_id]
    print("Executing '" + card['name'] + "'. Gonna curl '" + card['url'] + "'")
    # urllib.request.urlopen(card['url'])
    urllib2.urlopen(card['url'])

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
reader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")


current_tag = ''

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status,TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

    # If a card is found
    if status != reader.MI_OK:
        continue
        # print "Card detected"

    # Get the UID of the card
    (status,uid) = reader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == reader.MI_OK:

        # Print UID
        # print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
        tag_id = ''.join((str(x) for x in uid))

        if current_tag == tag_id:
            continue

        current_tag = tag_id

        # print('Tag detected: ' + tag_id)
        execute_id(tag_id)



