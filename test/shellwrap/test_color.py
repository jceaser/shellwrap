#from unittest.mock import Mock
#from unittest.mock import patch
import unittest

#import urllib.error as urlerr

#import test.util as tutil

import shellwrap.color as color

class TestColor(unittest.TestCase):
    """Test suit for Search API"""

    def pattern_maker_color(self, color, content):
        return '\033[0;{}m{}\033[0m'.format(color, content)
    def pattern_maker_style(self, color, content):
        return '{}{}\033[0m'.format(color, content)

    # **********************************************************************
    # Tests

    def test_tcode(self):
        def are(code_name, iscolor=True):
            expected_code = color.tcode[code_name]
            expected_esc = expected_code # assume style, not color
            if iscolor:
                expected_esc = '\x1b[0;{}m'.format(expected_code)
            expected_full = '\x1b[{};{}m'.format(expected_code, expected_code)
            self.assertEqual(expected_esc, color.tcode.__getattr__(code_name), "[] test")
            self.assertEqual(expected_code, color.tcode.raw(code_name), "raw() test")
            self.assertEqual(expected_full, color.tcode.full(code_name, code_name), "Full() test")

        are("red")
        are("green")
        are("backgreen")
        are("bright_yellow")
        are("underline", False)
        are("off_inverse", False)

    def test_red(self):
        src = lambda a : a
        self.assertEqual("\x1b[0;31mtest\x1b[0m", color.red(src)("test"))
        self.assertEqual(self.pattern_maker_color(color.tcode.raw('red'), "test"),
            color.red(src)("test"))

    def test_link(self):
        self.assertEqual('\x1b]8;;http://example.org\x07Example\x1b]8;;\x07',
            color.link("http://example.org", "Example"))

    def test_other(self):
        expected = self.pattern_maker_style(color.tcode.raw('hide'), "test")
        actual = color.encoder(color.tcode.hide, "test")
        self.assertEqual(expected, actual)
