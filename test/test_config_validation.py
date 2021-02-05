#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from assertpy import assert_that
from config import validate_config


class ValidateConfigTestCase(unittest.TestCase):

    @staticmethod
    def test_valid_config():
        # given
        config = {
            "1": {
                "name": "valid config",
                "ondetect": [
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=playplaylist&name=single_event",
                    }
                ]
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_true()

    @staticmethod
    def test_invalid_tag_id():
        # given
        config = {
            "invalid_tag_id": "hello"
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_invalid_tag_value():
        # given
        config = {
            "2": "invalid_tag_value"
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_invalid_tag_property():
        # given
        config = {
            "3": {
                "invalid_property": "nonono"
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_missing_tag_property_ondetect():
        # given
        config = {
            "4": {
                "name": "a nice tag name"
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_missing_tag_property_name():
        # given
        config = {
            "5": {
                "ondetect": []
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_tag_wrong_type_name():
        # given
        config = {
            "6": {
                "name": 1,
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
        assert_that(result).is_false()

    @staticmethod
    def test_tag_wrong_type_ondetect():
        # given
        config = {
            "7": {
                "name": "cool tag",
                "ondetect": "not okay"
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_tag_wrong_type_onremove():
        # given
        config = {
            "8": {
                "name": "cool tag",
                "ondetect": [],
                "onremove": "not okay"
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_tag_wrong_type_onredetect():
        # given
        config = {
            "9": {
                "name": "cool tag",
                "ondetect": [],
                "onredetect": "not okay"
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_event_combination_with_onremove():
        # given
        config = {
            "10": {
                "name": "cool tag",
                "ondetect": [],
                "onremove": []
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_true()

    @staticmethod
    def test_event_combination_with_onredetect():
        # given
        config = {
            "11": {
                "name": "cool tag",
                "ondetect": [],
                "onredetect": []
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_true()

    @staticmethod
    def test_event_combination_all():
        # given
        config = {
            "12": {
                "name": "cool tag",
                "ondetect": [],
                "onremove": [],
                "onredetect": []
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_true()

    @staticmethod
    def test_invalid_tag_extra_property():
        # given
        config = {
            "13": {
                "name": "cool tag",
                "ondetect": [],
                "not valid": "no no no"
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_invalid_actions_type():
        # given
        config = {
            "14": {
                "name": "cool tag",
                "ondetect": ["should be object", 10],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_curl_unkown_property():
        # given
        config = {
            "15": {
                "name": "cool tag",
                "ondetect": [{
                    "type": "curl",
                    "url": "http://bla.com",
                    "invalid": "No No No"
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_curl_url_must_be_uri():
        # given
        config = {
            "16": {
                "name": "cool tag",
                "ondetect": [{
                    "type": "curl",
                    "url": "not an uri",
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_command_unkown_property():
        # given
        config = {
            "17": {
                "name": "cool tag",
                "ondetect": [{
                    "type": "command",
                    "command": "ps awwwx",
                    "invalid": "No No No"
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_unknown_action():
        # given
        config = {
            "18": {
                "name": "cool tag",
                "ondetect": [{
                    "type": "unknow",
                    "url": "http://bla.com",
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_invalid_actions_type_onremove():
        # given
        config = {
            "19": {
                "name": "cool tag",
                "ondetect": [],
                "onremove": ["should be object", 10],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_curl_unkown_property_onremove():
        # given
        config = {
            "20": {
                "name": "cool tag",
                "ondetect": [],
                "onremove": [{
                    "type": "curl",
                    "url": "http://bla.com",
                    "invalid": "No No No"
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_curl_url_must_be_uri_onremove():
        # given
        config = {
            "21": {
                "name": "cool tag",
                "ondetect": [],
                "onremove": [{
                    "type": "curl",
                    "url": "not an uri",
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_command_unkown_property_onremove():
        # given
        config = {
            "22": {
                "name": "cool tag",
                "ondetect": [],
                "onremove": [{
                    "type": "command",
                    "command": "ps awwwx",
                    "invalid": "No No No"
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_unknown_action_onremove():
        # given
        config = {
            "23": {
                "name": "cool tag",
                "ondetect": [],
                "onremove": [{
                    "type": "unknow",
                    "url": "http://bla.com",
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_invalid_actions_type_onredetect():
        # given
        config = {
            "24": {
                "name": "cool tag",
                "ondetect": [],
                "onredetect": ["should be object", 10],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_curl_unkown_property_onredetect():
        # given
        config = {
            "25": {
                "name": "cool tag",
                "ondetect": [],
                "onredetect": [{
                    "type": "curl",
                    "url": "http://bla.com",
                    "invalid": "No No No"
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_curl_url_must_be_uri_onredetect():
        # given
        config = {
            "26": {
                "name": "cool tag",
                "ondetect": [],
                "onredetect": [{
                    "type": "curl",
                    "url": "not an uri",
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_action_command_unkown_property_onredetect():
        # given
        config = {
            "27": {
                "name": "cool tag",
                "ondetect": [],
                "onredetect": [{
                    "type": "command",
                    "command": "ps awwwx",
                    "invalid": "No No No"
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_unknown_action_onredetect():
        # given
        config = {
            "28": {
                "name": "cool tag",
                "ondetect": [],
                "onredetect": [{
                    "type": "unknow",
                    "url": "http://bla.com",
                }],
            }
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()


if "__main__" == __name__:
    unittest.main(verbosity=4)
