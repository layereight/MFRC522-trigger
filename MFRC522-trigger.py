#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pirc522
import sys
import os
import urllib.request
import time
import json
import logging
import logging.config
import logging.handlers
from enum import Enum, unique

logging.config.fileConfig(os.path.dirname(__file__) + '/logging.ini')
config = json.load(open(os.path.dirname(__file__) + '/config.json', encoding="utf-8"))


@unique
class NfcEvent(Enum):
    DETECT = 1
    REMOVE = 2
    REDETECT = 3


def execute_action(event: NfcEvent, tag_id: str):
    if tag_id not in config:
        logging.warning("No mapping for tag " + tag_id)
        return
    logging.debug("Action " + event.name + " for tag " + tag_id)
    card = config[tag_id]

    event_to_key_map = {
        NfcEvent.DETECT : "url",
        NfcEvent.REMOVE : "onremove",
        NfcEvent.REDETECT: "onredetect" if "onredetect" in card else "url"
    }

    key = event_to_key_map[event]

    if key not in card:
        logging.debug("No event key '" + key + "' for tag " + tag_id)
        return

    logging.info("Executing '" + card['name'] + "'[" + key + "]. Gonna curl '" + card[key] + "'")

    try:
        urllib.request.urlopen(card[key])
    except Exception:
        logging.error("Unable to open url " + card[key], sys.exc_info()[0])


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
            execute_action(NfcEvent.REMOVE, current_tag)
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

        # execute an action for the reading tag
        execute_action(NfcEvent.REDETECT if current_tag == last_tag else NfcEvent.DETECT, tag_id)

        last_tag = current_tag
    except KeyboardInterrupt:
        logging.info("Shutdown!")
        break
    except Exception:
        logging.exception("Unexpected exception '%s' occurred!", str(sys.exc_info()[0].__name__))
        break

reader.cleanup()
