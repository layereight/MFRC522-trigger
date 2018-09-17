#!/usr/bin/python
# -*- coding: utf8 -*-

import pirc522
import sys
import urllib2
import time
import json


config = json.loads(open('config.json', mode='r').read())


def execute_action(tag_id):
    if tag_id not in config:
        print("No mapping for tag " + tag_id)
        return
    # print("CARD_ID " + card_id)
    card = config[tag_id]
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
