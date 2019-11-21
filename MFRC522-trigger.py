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


def execute_action(action, tag_id):
    logging.debug("Action " + action + " for tag " + tag_id)
    if tag_id not in config:
        logging.warning("No mapping for tag " + tag_id)
        return
    logging.debug("CARD_ID " + tag_id)
    card = config[tag_id]

    mapped_action = action
    if action not in card and action == "onredetect":
        mapped_action = "url"
    elif action not in card:
        logging.debug("No action " + action + " for tag " + tag_id)
        return

    logging.info("Executing '" + card['name'] + "'[" + mapped_action + "]. Gonna curl '" + card[mapped_action] + "'")

    try:
        urllib2.urlopen(card[mapped_action])
    except:
        logging.error("Unable to open url " + card['url'], sys.exc_info()[0])


# welcome message
logging.info("Welcome to MFRC522-trigger!")
logging.info("Press Ctrl-C to stop.")

# create a reader
reader = pirc522.RFID()

current_tag = ''
last_tag = ''
count = 0
polling = False

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while True:
    try:
        # wait for reader to send an interrupt
        if not polling:
            reader.wait_for_tag()

        count += 1
        logging.debug("Reader loop %d", count)

        # scan for cards
        if not polling:
            (error, tag_type) = reader.request()

            # on error continue and retry
            if error:
                # logging.info("error request")
                polling = False
                continue

        # get the UID of the card
        (error, uid) = reader.anticoll()

        # on error continue and retry
        if error:
            # logging.info("error anticoll")
            execute_action("onremove", current_tag)
            current_tag = ''
            polling = False
            continue

        # transform UID into string representation
        tag_id = ''.join((str(x) for x in uid))

        polling = True

        # when we're still reading the same tag
        if current_tag == tag_id:
            # don't busy wait while there's a rfid tag near the reader
            time.sleep(0.1)
            continue

        current_tag = tag_id

        action = "onredetect" if current_tag == last_tag else "url"

        # execute an action for the reading tag
        execute_action(action, tag_id)

        last_tag = current_tag
    except KeyboardInterrupt:
        logging.info("Shutdown!")
        break
    except Exception:
        logging.exception("Unexpected exception '%s' occurred!", str(sys.exc_info()[0].__name__))
        break

reader.cleanup()
