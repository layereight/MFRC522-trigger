#!/usr/bin/env python3
# -*- coding: utf8 -*-


import pirc522
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# welcome message
eprint("Welcome to id-convert!")
eprint("Press Ctrl-C to stop.")

# create a reader
reader = pirc522.RFID()

found_tags = {}

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while True:
    try:
        # wait for reader to send an interrupt
        reader.wait_for_tag()

        # scan for cards
        (error, tag_type) = reader.request()

        # on error continue and retry
        if error:
            # eprint("error request")
            continue

        # get the UID of the card
        (error, uid_old) = reader.anticoll()

        # on error continue and retry
        if error:
            # eprint("error anticoll")
            continue

        uid_new = reader.read_id(as_number=False)

        if uid_new is None:
            # eprint("error read_id")
            continue

        # transform UID into string representation
        tag_id_old = ''.join((str(x) for x in uid_old))
        tag_id_new = ':'.join(x.to_bytes(1, 'big').hex() for x in uid_new).upper()

        if tag_id_new not in found_tags:
            print(tag_id_old + "_" + tag_id_new, flush=True)
            found_tags[tag_id_new] = 1
        else:
            eprint("Already got it! " + str(len(found_tags)))

    except KeyboardInterrupt:
        eprint("Shutdown!")
        break
    except Exception:
        eprint("Unexpected exception '%s' occurred!", str(sys.exc_info()[0].__name__))
        break

reader.cleanup()
