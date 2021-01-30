#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from assertpy import assert_that
import actions


class ResolveMultiActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.config = {
            "11": {
                "name": "multi_action",
                "ondetect": [
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=playplaylist&name=detect"
                    },
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=volume&volume=10"
                    }
                ],
                "onremove": [
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=playplaylist&name=remove"
                    },
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=volume&volume=50"
                    }
                ],
                "onredetect": [
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=playplaylist&name=redetect"
                    },
                    {
                        "type": "command",
                        "command": "dostuff_onredetect.sh"
                    },
                    {
                        "type": "curl",
                        "url": "http://localhost:3000/?cmd=volume&volume=100"
                    }
                ],
            }
        }

    def test_resolve_multiple_actions_on_detect(self):
        # given
        event = actions.NfcEvent.DETECT
        tag_id = "11"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(2)
        assert_that(result).contains_only(
            {"type": "curl", "url": "http://localhost:3000/?cmd=playplaylist&name=detect"},
            {"type": "curl", "url": "http://localhost:3000/?cmd=volume&volume=10"})

    def test_resolve_multiple_actions_on_remove(self):
        # given
        event = actions.NfcEvent.REMOVE
        tag_id = "11"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(2)
        assert_that(result).contains_only(
            {"type": "curl", "url": "http://localhost:3000/?cmd=playplaylist&name=remove"},
            {"type": "curl", "url": "http://localhost:3000/?cmd=volume&volume=50"})

    def test_resolve_multiple_actions_on_redetect(self):
        # given
        event = actions.NfcEvent.REDETECT
        tag_id = "11"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(3)
        assert_that(result).contains_only(
            {"type": "curl", "url": "http://localhost:3000/?cmd=playplaylist&name=redetect"},
            {"type": "command", "command": "dostuff_onredetect.sh"},
            {"type": "curl", "url": "http://localhost:3000/?cmd=volume&volume=100"})


if "__main__" == __name__:
    unittest.main(verbosity=4)
