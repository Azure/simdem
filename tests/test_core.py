# -*- coding: utf-8 -*-
""" Advanced test cases for SimDem """

import configparser
import os.path
import unittest

from .context import bash, codeblock, demo, simdem


class SimDemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    test_file = 'scratch/foo'
    simdem = None
    markdown_parser = None

    def setUp(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        config = configparser.ConfigParser()
        config.read('content/config/unit_test.ini')
        self.markdown_parser = codeblock.CodeBlockParser()
        self.simdem = simdem.Core(config, demo.Demo(config),
                                  self.markdown_parser, bash.BashExecutor())

    def test_run_cmd(self):
        """ Validate running a command only prints out the result """
        self.assertEqual("foobar\n", self.simdem.run_cmd('echo foobar'))

    def test_run_blocks(self):
        """ Validate running a document that creates a file actually creates it """
        self.assertFalse(os.path.exists(self.test_file))
        blocks = self.markdown_parser.parse_file('content/create-file/README.md')
        self.simdem.run_blocks(blocks['commands'])
        self.assertTrue(os.path.exists(self.test_file))

if __name__ == '__main__':
    unittest.main()
