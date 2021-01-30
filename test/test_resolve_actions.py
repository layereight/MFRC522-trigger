#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from assertpy import assert_that
import actions


class ResolveActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.config = {
            "111": {
                "name": "single_event",
                "ondetect": {
                    "type": "curl",
                    "url": "http://localhost:3000/?cmd=playplaylist&name=single_event"
                }
            },
            "222": {
                "name": "detect_remove",
                "ondetect" : {
                    "type": "curl",
                    "url": "http://localhost:3000/?cmd=pause&name=detect_remove"
                },
                "onremove": {
                    "type": "curl",
                    "url": "http://localhost:3000/?cmd=play&name=detect_remove"
                }
            },
            "333": {
                "name": "all_events",
                "ondetect" : {
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

    def test_tag_is_not_configured(self):
        # given
        event = actions.NfcEvent.DETECT
        tag_id = "666"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_empty()

    def test_resolve_action_for_simple_config_on_detect(self):
        # given
        event = actions.NfcEvent.DETECT
        tag_id = "111"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=playplaylist&name=single_event"})

    def test_resolve_action_for_simple_config_on_redetect(self):
        # given
        event = actions.NfcEvent.REDETECT
        tag_id = "111"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=playplaylist&name=single_event"})

    def test_resolve_action_for_simple_config_on_remove(self):
        # given
        event = actions.NfcEvent.REMOVE
        tag_id = "111"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_empty()

    def test_resolve_action_for_extended_config_on_detect(self):
        # given
        event = actions.NfcEvent.DETECT
        tag_id = "222"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=pause&name=detect_remove"})

    def test_resolve_action_for_extended_config_on_redetect(self):
        # given
        event = actions.NfcEvent.REDETECT
        tag_id = "222"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=pause&name=detect_remove"})

    def test_resolve_action_for_extended_config_on_remove(self):
        # given
        event = actions.NfcEvent.REMOVE
        tag_id = "222"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=play&name=detect_remove"})

    def test_resolve_action_for_full_config_on_detect(self):
        # given
        event = actions.NfcEvent.DETECT
        tag_id = "333"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=playplaylist&name=all_events"})

    def test_resolve_action_for_full_config_on_redetect(self):
        # given
        event = actions.NfcEvent.REDETECT
        tag_id = "333"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=play&name=all_events"})

    def test_resolve_action_for_full_config_on_remove(self):
        # given
        event = actions.NfcEvent.REMOVE
        tag_id = "333"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=pause&name=all_events"})

    def test_resolve_action_for_legacy_config_on_detect(self):
        # given
        event = actions.NfcEvent.DETECT
        tag_id = "444"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=playplaylist&name=legacy_config"})

    def test_resolve_action_for_legacy_config_on_redetect(self):
        # given
        event = actions.NfcEvent.REDETECT
        tag_id = "444"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_length(1)
        assert_that(result).contains_only({"type": "curl", "url": "http://localhost:3000/?cmd=playplaylist&name=legacy_config"})

    def test_resolve_action_for_legacy_config_on_remove(self):
        # given
        event = actions.NfcEvent.REMOVE
        tag_id = "444"

        # when
        result = actions.resolve(self.config, event, tag_id)

        # then
        assert_that(result).is_empty()


if "__main__" == __name__:
    unittest.main(verbosity=4)
