#!/usr/bin/env python3
# -*- coding: utf8 -*-
from enum import Enum, unique

@unique
class NfcEvent(Enum):
    DETECT = 1
    REMOVE = 2
    REDETECT = 3


def resolve_actions(config: dict, event: NfcEvent, tag_id: str):
    if tag_id not in config:
        # logging.warning("No mapping for tag " + tag_id)
        return []

    # logging.debug("Action " + event.name + " for tag " + tag_id)
    card = config[tag_id]

    event_to_key_map = {
        NfcEvent.DETECT: "ondetect" if "ondetect" in card else "url",
        NfcEvent.REMOVE: "onremove",
        NfcEvent.REDETECT: "onredetect" if "onredetect" in card else "ondetect" if "ondetect" in card else "url"
    }

    key = event_to_key_map[event]

    if key not in card:
        # logging.debug("No event key '" + key + "' for tag " + tag_id)
        return []

    # logging.info("Executing '" + card['name'] + "'[" + key + "].")

    if type(card[key]) is dict:
        action = card[key]

        # ACTION_MAP[action["type"]](action)
        return [action]

    return [ {"type": "curl", "url": card[key]} ]
