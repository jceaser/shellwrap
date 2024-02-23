#from unittest.mock import Mock
#from unittest.mock import patch
import unittest

#import urllib.error as urlerr
#import test.util as tutil

import shellwrap.util as util

class TestColor(unittest.TestCase):

    def test_json(self):
        """ Setup a function to cgall str_to_json on """
        @util.str_to_json
        def foo(data):
            """This function could load a file and return a JSON string"""
            return  "{\"Data\": \"%s\"}" % data

        expected = {'Data': 'test'}
        actual = foo("test")
        self.assertEqual(expected, actual)
