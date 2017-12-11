# -*- coding: utf-8 -*-

from .context import simdem, demo

import unittest
import os.path
import configparser
import mistune

class SimDemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    test_file = '/tmp/foo'
    simdem = None
    parser = None

    def setUp(self):
        os.remove(self.test_file) if os.path.exists(self.test_file) else None
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")
        self.parser = simdem.Parser(mistune.BlockLexer())
        self.simdem = simdem.Core(config, demo.Demo(config), self.parser)

    def test_run_cmd(self):
        self.assertEquals("foobar\n", self.simdem.run_cmd('echo foobar'))
    
    def test_run_blocks(self):
        doc = """this is text
```shell
touch %(file)s```
more text""" % { 'file' : self.test_file }
        
        self.assertFalse(os.path.exists(self.test_file))
        blocks = self.parser.parse_doc(doc)
        self.simdem.run_blocks(blocks)
        self.assertTrue(os.path.exists(self.test_file))

if __name__ == '__main__':
    unittest.main()
