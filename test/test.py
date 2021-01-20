#!/usr/bin/env -S python -m pytest 
from io import StringIO
from subprocess import Popen, PIPE
import code
import os
from os import path as op
import re
import sys
import unittest

days = ['Monday', 'Tuesday', 'Wednesday', \
        'Thursday', 'Friday', 'Saturday', 'Sunday']
days_abbrev = [d[:3] for d in days]

ISO_FORMAT = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$'

YMD_FORMAT = r'^\d{4}-\d{2}-\d{2}$'

HMS_FORMAT = r'^\d+:\d+:\d+$'

test_expectancy = {
        '(T-1d).dow'                : lambda r: r in days,
        '-1d.dow'                   : lambda r: r in days,
        '08h30'                     : lambda r: r == '8:30:00',
        '1-1-1-1-1-1'               : lambda r: re.match(HMS_FORMAT, r),
        '1610494238'                : lambda r: r == '2021-01-12 20:30:38',
        '1610494238+4h.dow'         : lambda r: r == 'Wednesday',
        '1610494238.dow'            : lambda r: r == 'Tuesday',
        '1958-05-14 - 1958-05-16'   : lambda r: r == '-2 days, 0:00:00',
        '1996.04.28'                : lambda r: r == '1996-04-28',
        '1d'                        : lambda r: r == '1 day, 0:00:00',
        '1d+0h22M'                  : lambda r: r == '1 day, 0:22:00',
        '1w'                        : lambda r: r == '7 days, 0:00:00',
        '2 < 1'                     : lambda r: not eval(r),
        '22h+2M'                    : lambda r: r == '22:02:00', 
        '22h22M'                    : lambda r: r == '22:22:00', 
        '2h2M'                      : lambda r: r == '2:02:00',
        '3h+3m'                     : lambda r: r.startswith('90 days, 2:59:59'), 
        '3m'                        : lambda r: r.startswith('89 days, 23:59:59'),
        'T-1.5d'                    : lambda r: re.match(YMD_FORMAT, r),
        'T-10d'                     : lambda r: re.match(YMD_FORMAT, r),
        'T.day'                     : lambda r: 0 < int(r) < 32,
        'T.dow'                     : lambda r: r in days,
        'YD.day'                    : lambda r: re.match(r'\d+', r),
        'next Sunday'               : lambda r: re.match(YMD_FORMAT, r),
        'wait .001s'                : lambda r: len(r) == 0,
        'yd-5h'                     : lambda r: re.match(ISO_FORMAT, r),
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
    return output

class Tester(unittest.TestCase):

    def test_stuff(self):
        test_outputs = []
        dte_location = os.path.dirname(os.path.realpath(__file__)) \
                                 + op.sep + '..'   \
                                 + op.sep + 'dte' \
                                 + op.sep + 'dte'
        for test,expectancy in test_expectancy.items():
            p = Popen(dte_location, stdin=PIPE, stdout=PIPE)
            out,err = p.communicate(test.encode('utf-8'))
            out = out.decode('utf-8').replace('\n','')
            try:
                assert expectancy(out) and not err
            except Exception as e:
                print(test)
                raise e
