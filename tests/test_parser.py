# -*- coding: utf-8 -*-

from .context import simdem, demo

import unittest
import os.path
import configparser
import mistune

class SimDemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    test_file = '/tmp/foo'
    parser = None

    def setUp(self):
        os.remove(self.test_file) if os.path.exists(self.test_file) else None
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")

        self.parser = simdem.Parser()

    def test_parse_ref_from_text(self):
        self.assertEquals('./nested_prereq.md', self.parser.parse_ref_from_text('We should be able to run [nested prerequisites](./nested_prereq.md).'))
        
if __name__ == '__main__':
    unittest.main()
