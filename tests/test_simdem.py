# -*- coding: utf-8 -*-

from .context import simdem

import unittest
import os.path

class SimDemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    test_file = '/tmp/foo'

    def setUp(self):
        os.remove(self.test_file) if os.path.exists(self.test_file) else None

    def test_init(self):
        self.assertIsNone(simdem.start())
    
    def test_run_cmd(self):
        self.assertEquals("foobar\r\n", simdem.run_cmd('echo foobar'))
    
    def test_run_doc(self):
        doc = """this is text
```shell
touch %(file)s```
more text""" % { 'file' : self.test_file }
        
        self.assertFalse(os.path.exists(self.test_file))
        simdem.run_doc(doc)
        self.assertTrue(os.path.exists(self.test_file))


if __name__ == '__main__':
    unittest.main()
