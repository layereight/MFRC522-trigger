#!/usr/bin/python
# -*- coding: utf8 -*-

import pirc522
import sys
import urllib2
import time

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
        'name': "Löwe",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    },
    '13647223446': {
        'id': 13647223446,
        'name': "Zebra",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=Traumzauberbaum"
    },
    '1364223226177': {
        'id': 1364223226177,
        'name': "Giraffe",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=Kinderlieder"
    },
    '1364209227190': {
        'id': 1364209227190,
        'name': "Hyäne",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=SoaD"
    },
    '1364215226185': {
        'id': 1364215226185,
        'name': "Elefant",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=Traumzauberbaum"
    },
    '13648223553': {
        'id': 13648223553,
        'name': "Nilpferd",
        'url': "http://localhost:3000/api/v1/commands/?cmd=playplaylist&name=Kinderlieder"
    }
}

def execute_action(tag_id):
    if tag_id not in map:
        print("No mapping for tag " + tag_id)
        return
    # print("CARD_ID " + card_id)
    card = map[tag_id]
    print("Executing '" + card['name'] + "'. Gonna curl '" + card['url'] + "'")
    try:
        urllib2.urlopen(card['url'])
    except:
        print("Unable to open url " + card['url'], sys.exc_info()[0])


# welcome message
print("Welcome to MFRC522-trigger!")
print("Press Ctrl-C to stop.")

# create a reader
reader = pirc522.RFID()

current_tag = ''
count = 0

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while True:
    try:
        # don't busy wait while there's a rfid tag near the reader
        time.sleep(1)


        # wait for reader to send an interrupt
        reader.wait_for_tag()

        count += 1
        print("reading " + str(count))

        # scan for cards
        (error, tag_type) = reader.request()

        # on error continue and retry
        if error:
            continue

        # get the UID of the card
        (error, uid) = reader.anticoll()

        # on error continue and retry
        if error:
            continue

        # transform UID into string representation
        tag_id = ''.join((str(x) for x in uid))

        # when we're still reading the same tag
        if current_tag == tag_id:
            continue

        current_tag = tag_id

        # execute an action for the reading tag
        execute_action(tag_id)
    except:
        print("Shutdown!")
        break

reader.cleanup()
