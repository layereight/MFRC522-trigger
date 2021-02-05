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
            "222": "invalid_tag_value"
        }

        # when
        result = validate_config(config)

        # then
        assert_that(result).is_false()

    @staticmethod
    def test_invalid_tag_property():
        # given
        config = {
            "333": {
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
            "444": {
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
            "555": {
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
            "666": {
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
            "777": {
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
            "888": {
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
            "999": {
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
            "000": {
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
            "1111": {
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
            "2222": {
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


if "__main__" == __name__:
    unittest.main(verbosity=4)
