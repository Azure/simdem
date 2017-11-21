# -*- coding: utf-8 -*-

from .context import simdem
from mistune import Renderer, InlineGrammar, InlineLexer

import mistune
import unittest


class LexerTestSuite(unittest.TestCase):
    """Lexer test cases."""

    def test_mistune(self):
        res = mistune.markdown('I am using **mistune markdown parser**')
        self.assertEquals(res, "<p>I am using <strong>mistune markdown parser</strong></p>\n")

    def test_block_lexer(self):
        blockLexer = mistune.BlockLexer()
        res = blockLexer.parse('I am using **mistune markdown parser**')
        self.assertEquals(res, [{'type': 'paragraph', 'text': 'I am using **mistune markdown parser**'}])

    def test_block_lexer_cmd(self):
        blockLexer = mistune.BlockLexer()
        res = blockLexer.parse("```php\necho $foo```")
        self.assertEquals(res, [{'lang': 'php', 'text': 'echo $foo', 'type': 'code'}])

    def test_block_lexer_multiline(self):
        blockLexer = mistune.BlockLexer()
        res = blockLexer.parse("""this is text
```shell
echo $FOO```
more text""")
        self.assertEquals(res, [{'type': 'paragraph', 'text': 'this is text'},
            {'lang': 'shell', 'text': 'echo $FOO', 'type': 'code'},
            {'text': 'more text', 'type': 'paragraph'}])

    '''
    Haven't figured this out yet.
    def test_inline_lexer(self):
        inlineLexer = mistune.InlineLexer()
        res = inlineLexer.parse('I am using **mistune markdown parser**')
        self.assertEquals(res, [{'type': 'paragraph', 'text': 'I am using **mistune markdown parser**'}])
    '''

if __name__ == '__main__':
    unittest.main()
