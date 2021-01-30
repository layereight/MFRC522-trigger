#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from assertpy import assert_that
from actions import actions


class ResolveActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.config = {
            "123": {
                "name": "some tag",
                "ondetect": {
                    "type": "curl",
                    "command": "http://localhost:3000"
                }
            }
        }

    def test_resolve_single_action(self):
        # given
        event = actions.NfcEvent.DETECT
        tag_id = "123"

        # when
        result = actions.resolve_actions(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "command": "http://localhost:3000"})


if "__main__" == __name__:
    unittest.main(verbosity=4)
