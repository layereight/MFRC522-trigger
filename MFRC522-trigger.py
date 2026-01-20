#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pirc522
import sys
from os import path
import urllib.request
import subprocess
import time
import json
import logging
import logging.config
import logging.handlers

from actions import NfcEvent, resolve
from config import validate_config

pathname = path.dirname(path.abspath(__file__))
logging.config.fileConfig(pathname + '/logging.ini')
config = json.load(open(pathname + '/config.json', encoding="utf-8"))


def execute_curl(url):
    logging.info("Gonna curl '" + url + "'")
    try:
        urllib.request.urlopen(url)
    except Exception:
        logging.error("Unable to open url " + url, sys.exc_info()[0])


def execute_command(command):
    logging.info("Gonna execute '" + command + "'")
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)


ACTION_MAP = {
    "curl": lambda action: execute_curl(action["url"]),
    "command": lambda action: execute_command(action["command"])
}


def execute_action(event: NfcEvent, tag_id: str):

    resolved_actions = resolve(config, event, tag_id)

    for action in resolved_actions:
        ACTION_MAP[action["type"]](action)


def tag_id_from_bytes(uid):
    return ':'.join(x.to_bytes(1, 'big').hex() for x in uid).upper()


# welcome message
logging.info("Welcome to MFRC522-trigger!")

if not validate_config(config):
    sys.exit(1)

logging.info("Press Ctrl-C to stop.")

# create a reader
reader = pirc522.RFID()

current_nuid = ''

current_tag = ''
last_tag = ''
count = 0
polling = False

last_was_7_byte_id = False

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while True:
    try:
        # wait for reader to send an interrupt
        if not polling:
            # reader.wait_for_tag()
            logging.debug("Sleep!")
            time.sleep(0.5)

        count += 1
        logging.debug("Reader loop %d", count)

        # scan for cards
        if not polling or last_was_7_byte_id:
            (error, tag_type) = reader.request()

            # on error continue and retry
            if error:
                logging.debug("error request")
                if current_tag != '':
                    execute_action(NfcEvent.REMOVE, current_tag)
                    current_tag = ''
                current_nuid = ''

                polling = False
                continue

        # reset after request
        last_was_7_byte_id = False

        # get the UID of the card
        (error, uid) = reader.anticoll()

        # on error continue and retry
        if error:
            logging.debug("error anticoll")
            if current_tag != '':
                execute_action(NfcEvent.REMOVE, current_tag)
                current_tag = ''
            current_nuid = ''
            polling = False
            continue

        nuid = tag_id_from_bytes(uid)

        got_uid = True
        tag_id = ''

        # Do we have an incomplete UID?!
        if uid[0] != 0x88:
            got_uid = False
            tag_id = tag_id_from_bytes(uid[0:4])

        if got_uid and (current_nuid != nuid):
            # Activate the tag with the incomplete UID
            error = reader.select_tag(uid)
            if error:
                logging.debug("error select_tag")
                polling = False
                continue

            # Get the remaining bytes
            error, uid2 = reader.anticoll2()
            if error:
                logging.debug("error anticoll2")
                polling = False
                continue

            reader.halt()
            last_was_7_byte_id = True

            # Build the final UID without checksums
            tag_id = tag_id_from_bytes(uid[1:-1] + uid2[:-1])

        logging.debug("Tag ID: " + tag_id)

        polling = True

        # when we're still reading the same tag
        if current_nuid == nuid:
            # don't busy wait while there's a rfid tag near the reader
            logging.debug("Sleep!")
            time.sleep(0.1)
            continue

        current_tag = tag_id
        current_nuid = nuid

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
