#!/usr/bin/env -S python -m pytest 
from mtc import *
import sys
from io import StringIO
import code
import unittest

test_expectancy = {
        'T-10d' : lambda r: len(r) == 26,
        }

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def parse(test):
    with Capturing() as output:
        yacc.parse(test)
    return output[0]

class Tester(unittest.TestCase):

    def test_stuff(self):
        test_outputs = []
        for test,expectancy in test_expectancy.items():
            assert expectancy(parse(test))
