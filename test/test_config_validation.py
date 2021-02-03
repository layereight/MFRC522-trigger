#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from assertpy import assert_that
from config import validate_config


class ValidateConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = {
            "111": {
                "name": "single_event",
                "ondetect": [
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=playplaylist&name=single_event"
                    }
                ]
            },
            "222": {
                "name": "detect_remove",
                "ondetect": [
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=pause&name=detect_remove"
                    }
                ],
                "onremove": [
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=play&name=detect_remove"
                    }
                ]
            },
            "333": {
                "name": "all_events",
                "ondetect": {
                    "type": "curl",
                    "url": "http://localhost:3000/?cmd=playplaylist&name=all_events"
                },
                "onremove": {
                    "type": "curl",
                    "url": "http://localhost:3000/?cmd=pause&name=all_events"
                },
                "onredetect": {
                    "type": "curl",
                    "url": "http://localhost:3000/?cmd=play&name=all_events"
                }
            },
            "444": {
                "name": "legacy_config",
                "url": "http://localhost:3000/?cmd=playplaylist&name=legacy_config"
            }
        }

    def test_valid_config(self):
        # given
        config = {
            "111": {
                "name": "valid config",
                "ondetect": [
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=playplaylist&name=single_event"
                    }
                ]
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_true()

    def test_invalid_config(self):
        # given
        config2 = {
            "invalid_tag_id": "hello"
        }

        # when
        result = validate_config(config2)

        # then
        assert_that(result).is_false()



if "__main__" == __name__:
    unittest.main(verbosity=4)
