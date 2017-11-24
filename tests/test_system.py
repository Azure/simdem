# -*- coding: utf-8 -*-

from .context import simdem, demo

import unittest
import configparser
import mistune
import sys
from ddt import ddt,data

@ddt
class SimDemSystemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    simdem = None

    def setUp(self):
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")
        self.simdem = simdem.Core(config, demo.Demo(config), mistune.BlockLexer())

    # https://docs.python.org/3/library/unittest.html#unittest.TestResult.buffer
    @data('simple', 'simple-variable')
    def test_process(self, dir):
        self.simdem.process_file('./content/' + dir + '/README.md')
        res = sys.stdout.getvalue()
        exp_res = open('./content/' + dir + '/expected_result.out', 'r').read()
        self.assertEquals(exp_res, res)


if __name__ == '__main__':
    unittest.main()
