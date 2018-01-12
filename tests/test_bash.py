# -*- coding: utf-8 -*-
""" Advanced test cases for SimDem """

import unittest

from simdem.executor import bash

class SimDemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    bash = None

    def setUp(self):
        self.bash = bash.BashExecutor()

    def test_run_cmd(self):
        """ Validate running a command only prints out the result """
        self.assertEqual("foobar\n", self.bash.run_cmd('echo foobar'))


if __name__ == '__main__':
    unittest.main()
