# -*- coding: utf-8 -*-

from .context import simdem, demo

import unittest
import os.path
import configparser
import mistune

class SimDemParserTestSuite(unittest.TestCase):
    """Advanced test cases."""

    parser = None

    def setUp(self):
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")

        self.parser = simdem.Parser(mistune.BlockLexer())

    def test_parse_ref_from_text(self):
        self.assertEquals('./nested_prereq.md', self.parser.parse_ref_from_text('We should be able to run [nested prerequisites](./nested_prereq.md).'))

    def test_parse_doc2(self):
        doc = """foo
# Prerequisites

prereq.md
prereq-2.md

# Do stuff here

We want to execute this because the code type is shell

```shell
echo foo
echo bar
```

# Do more stuff here

```shell
echo baz
```

# Results

The only thing that makes it a result is the code type is result.
We assume the result is for the last command of the last code block

```result
baz
```


"""
        exp_res = {
            'prerequisites': ['prereq.md', 'prereq-2.md'],
            'commands': [
                { 'command': 'echo foo' },
                { 'command': 'echo bar' },
                { 'command': 'echo baz', 'expected_result': 'baz' } ]
        }
        res = self.parser.parse_doc(doc)
        self.assertEquals(res, exp_res)

if __name__ == '__main__':
    unittest.main()
