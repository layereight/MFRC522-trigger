#!/usr/bin/python
# -*- coding: utf8 -*-

import pirc522
import sys
import os
import urllib2
import time
import json
import logging
import logging.config
import logging.handlers


logging.config.fileConfig(os.path.dirname(__file__) + '/logging.ini')
config = json.load(open(os.path.dirname(__file__) + '/config.json'))


def execute_action(tag_id):
    if tag_id not in config:
        logging.warning("No mapping for tag " + tag_id)
        return
    logging.debug("CARD_ID " + tag_id)
    card = config[tag_id]
    logging.info("Executing '" + card['name'] + "'. Gonna curl '" + card['url'] + "'")
    try:
        urllib2.urlopen(card['url'])
    except:
        logging.error("Unable to open url " + card['url'], sys.exc_info()[0])


# welcome message
logging.info("Welcome to MFRC522-trigger!")
logging.info("Press Ctrl-C to stop.")

# create a reader
reader = pirc522.RFID(speed=100)

current_tag = ''
count = 0

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while True:
    try:
        # don't busy wait while there's a rfid tag near the reader
        time.sleep(1)

        reader.init()

        # wait for reader to send an interrupt
        reader.wait_for_tag()

        count += 1
        logging.debug("Reader loop %d", count)

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
    except KeyboardInterrupt:
        logging.info("Shutdown!")
        break
    except Exception:
        logging.exception("Unexpected exception '%s' occurred!", str(sys.exc_info()[0].__name__))
        break

reader.cleanup()
