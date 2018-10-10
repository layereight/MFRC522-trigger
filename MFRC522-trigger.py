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
import multiprocessing
import ctypes


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


def reader_func(event, current_tag_id):

    # create a reader
    reader = pirc522.RFID()

    count = 0

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while True:
        try:
            # don't busy wait while there's a rfid tag near the reader
            time.sleep(1)

            # wait for reader to send an interrupt
            reader.wait_for_tag()

            event.set()

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
            if current_tag_id.value == tag_id:
                continue

            current_tag_id.value = tag_id

            # execute an action for the reading tag
            execute_action(tag_id)
        except KeyboardInterrupt:
            logging.info("Shutdown!")
            break
        except Exception:
            logging.exception("Unexpected exception '%s' occurred!", str(sys.exc_info()[0].__name__))
            break

    reader.cleanup()


supervisor_event = multiprocessing.Event()
manager = multiprocessing.Manager()
current_tag = manager.Value(ctypes.c_char_p, "")
reader_process = multiprocessing.Process(target=reader_func, args=(supervisor_event, current_tag))
reader_process.start()

while True:
    try:
        logging.debug("Supervisor loop")
        supervisor_event.wait(10)
        if not supervisor_event.is_set():
            logging.warn("Possibly blocked reader detected! Or no NFC tag within reach. Will re-create reader.")
            reader_process.terminate()
            reader_process = multiprocessing.Process(target=reader_func, args=(supervisor_event, current_tag))
            reader_process.start()
        supervisor_event.clear()
    except KeyboardInterrupt:
        logging.info("Shutdown!")
        break
    except Exception:
        logging.exception("Unexpected exception '%s' occurred!", str(sys.exc_info()[0].__name__))
        break




