# -*- coding: utf-8 -*-

from .context import simdem, demo

import unittest
import os.path
import configparser
import mistune
import sys

class SimDemSystemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    test_file = '/tmp/foo'
    simdem = None

    def setUp(self):
        os.remove(self.test_file) if os.path.exists(self.test_file) else None
        config = configparser.ConfigParser()
        config.read("../content/config/demo.ini")

        self.simdem = simdem.Core(config, demo.Demo(), mistune.BlockLexer())


    def test_process_file(self):
        self.simdem.process_file("./content/simple/README.md")
        res = sys.stdout.getvalue()
        exp_res = open('./content/simple/expected_result.out', 'r').read()
        self.assertEquals(open('./content/simple/expected_result.out', 'r').read(), res)

    def test_process_file2(self):
        self.simdem.process_file("./content/simple-variable/README.md")
        res = sys.stdout.getvalue()
        self.assertEquals(open('./content/simple-variable/expected_result.out', 'r').read(), res)

if __name__ == '__main__':
    unittest.main()
