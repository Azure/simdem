# -*- coding: utf-8 -*-
""" system level test class """

import configparser
import unittest
import json

from ddt import data, ddt

from simdem.parser import simdem1

@ddt
class SimDem1ParserTestSuite(unittest.TestCase):
    """Advanced test cases."""

    parser = None

    def setUp(self):
        config = configparser.ConfigParser()
        config.read("examples/config/unit_test.ini")

        self.parser = simdem1.SimDem1Parser()


    # https://docs.python.org/3/library/unittest.html#unittest.TestResult.buffer
    #@data('markdown-syntax')
    @data('simple', 'simple-variable', 'results-block',
          'results-block-fail', 'prerequisites')
    def test_process(self, directory):
        """ Each examples directory is expected to have a README.md and an expected_result.tutorial
            this allows us to test each of them easily
        """
        self.maxDiff = None # pylint: disable=C0103
        res = self.parser.parse_file('./examples/' + directory + '/README.md')

        # Research how to read dict from file
        exp_res = json.load(open('./examples/' + directory + '/expected_result.seo', 'r'))
        self.assertEqual(exp_res, res)


if __name__ == '__main__':
    unittest.main()
