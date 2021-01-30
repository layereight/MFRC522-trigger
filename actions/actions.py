#!/usr/bin/env python3
# -*- coding: utf8 -*-
from enum import Enum, unique
import logging


@unique
class NfcEvent(Enum):
    DETECT = 1
    REMOVE = 2
    REDETECT = 3


def resolve(config: dict, event: NfcEvent, tag_id: str):
    if tag_id not in config:
        logging.warning("No mapping for tag " + tag_id)
        return []

    # logging.debug("Action " + event.name + " for tag " + tag_id)
    config_tag = config[tag_id]

    event_to_key_map = {
        NfcEvent.DETECT: "ondetect" if "ondetect" in config_tag else "url",
        NfcEvent.REMOVE: "onremove",
        NfcEvent.REDETECT: "onredetect" if "onredetect" in config_tag else "ondetect" if "ondetect" in config_tag else "url"
    }

    event_key = event_to_key_map[event]

    if event_key not in config_tag:
        logging.debug("No event key '" + event_key + "' for tag " + tag_id)
        return []

    logging.info("Executing '" + config_tag['name'] + "'[" + event_key + "].")

    # configure list of actions
    if type(config_tag[event_key]) is list:
        return config_tag[event_key]
    # legacy: just one action
    elif type(config_tag[event_key]) is dict:
        return [config_tag[event_key]]
    # very legacy: just url
    else:
        return [{"type": "curl", "url": config_tag[event_key]}]
