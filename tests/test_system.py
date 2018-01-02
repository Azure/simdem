# -*- coding: utf-8 -*-

from .context import simdem, demo

import unittest
import os
import configparser
import mistune
import logging
import sys
from ddt import ddt,data

@ddt
class SimDemSystemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    simdem = None

    def setUp(self):

        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")
        self.simdem = simdem.Core(config, demo.Demo(config), simdem.parser.CodeBlockParser(), simdem.executor.BashExecutor())

        logFormatter = logging.Formatter(config.get('LOG', 'FORMAT', raw=True))
        rootLogger = logging.getLogger()
        rootLogger.setLevel(config.get('LOG', 'LEVEL'))
        fileHandler = logging.FileHandler(config.get('LOG', 'FILE'))
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

    # https://docs.python.org/3/library/unittest.html#unittest.TestResult.buffer
#    @data('prerequisite-run')
    @data('simple', 'simple-variable', 'results-block', 'results-block-fail', 'create-file', 'prerequisite-run')
    def test_process(self, dir):
        self.simdem.process_file('./content/' + dir + '/README.md')
        res = sys.stdout.getvalue()
        exp_res = open('./content/' + dir + '/expected_result.out', 'r').read()
        self.assertEquals(exp_res, res)


if __name__ == '__main__':
    unittest.main()
