# -*- coding: utf-8 -*-

from .context import simdem

import unittest
import os.path
import configparser

class SimDemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    test_file = '/tmp/foo'
    simdem = None

    def setUp(self):
        os.remove(self.test_file) if os.path.exists(self.test_file) else None
        config = configparser.ConfigParser()
        config.read("../content/config/demo.ini")

        self.simdem = simdem.Core(config)

    def test_run_cmd(self):
        self.assertEquals("foobar\r\n", self.simdem.run_cmd('echo foobar'))
    
    def test_run_doc(self):
        doc = """this is text
```shell
touch %(file)s```
more text""" % { 'file' : self.test_file }
        
        self.assertFalse(os.path.exists(self.test_file))
        self.simdem.run_doc(doc)
        self.assertTrue(os.path.exists(self.test_file))

    def test_process_file(self):
        res = self.simdem.process_file("./content/simple/README.md")
        self.assertTrue("$ echo foobar\nfoobar\n")


if __name__ == '__main__':
    unittest.main()
