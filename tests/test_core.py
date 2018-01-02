# -*- coding: utf-8 -*-

from .context import simdem, demo, bash, codeblock

import unittest
import os.path
import configparser
import mistune

class SimDemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    test_file = 'scratch/foo'
    simdem = None
    markdown_parser = None

    def setUp(self):
        os.remove(self.test_file) if os.path.exists(self.test_file) else None
        config = configparser.ConfigParser()
        config.read('content/config/unit_test.ini')
        self.markdown_parser = codeblock.CodeBlockParser()
        self.simdem = simdem.Core(config, demo.Demo(config), self.markdown_parser, bash.BashExecutor())

    def test_run_cmd(self):
        self.assertEquals("foobar\n", self.simdem.run_cmd('echo foobar'))
    
    def test_run_blocks(self):
        self.assertFalse(os.path.exists(self.test_file))
        blocks = self.markdown_parser.parse_file('content/create-file/README.md')
        self.simdem.run_blocks(blocks['commands'])
        self.assertTrue(os.path.exists(self.test_file))

if __name__ == '__main__':
    unittest.main()
