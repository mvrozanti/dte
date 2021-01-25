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

ISO_FORMAT = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?$'

YMD_FORMAT = r'^\d{4}-\d{2}-\d{2}$'

HMS_FORMAT = r'^\d+:\d+:\d+$'

DELTA_FORMAT = r'-?\d+ days, \d{1,2}:\d{2}:\d{2}'

test_expectancy = {
        '(T-1d).dow'                            : lambda r: r in days,
        '(n + 180d)-180d == n'                  : lambda r: eval(r),
        '(n + 181d)-180d != n'                  : lambda r: eval(r),
        '(t + 180d)-180d == t'                  : lambda r: eval(r),
        '-1d.dow'                               : lambda r: r in days,
        '08h30'                                 : lambda r: r == '8:30:00',
        '1 in unix'                             : lambda r: r == '1',
        '1-1-1 23:23:23'                        : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23:23M'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23h:23'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23h:23M'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23M:23'                          : lambda r: re.match(ISO_FORMAT, r),
        'n - 1234'                              : lambda r: re.match(DELTA_FORMAT, r),
        '1-1-1 23M:23s'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23M:23S'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23:23S'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1-1-1-1'                           : lambda r: re.match(HMS_FORMAT, r),
        '1610494238'                            : lambda r: '2021-01-12' in r,
        '1610494238+4h.dow'                     : lambda r: r == 'Wednesday',
        '1610494238.dow'                        : lambda r: r == 'Tuesday',
        '2014 Jan 13'                           : lambda r: r == '2014-01-13',
        '2014 January 13'                       : lambda r: r == '2014-01-13',
        '2014 Jan 13==2014 January 13'          : lambda r: eval(r),
        'help'                                  : lambda r: len(r) > 1500,
        '1957-12-26 - t'                        : lambda r: re.match(DELTA_FORMAT, r),
        '1957-12-26 22:22:22 - t'               : lambda r: re.match(DELTA_FORMAT, r),
        '1957-12-26 22:22:22 in unix'           : lambda r: -379118258 - 86400 < int(r) < -379118258 + 86400,
        '1958-05-14 - 1958-05-16'               : lambda r: r == '-2 days, 0:00:00',
        '1996.04.28'                            : lambda r: r == '1996-04-28',
        '1d in hours'                           : lambda r: r == '24.0',
        '1d in minutes'                         : lambda r: r == '1440.0',
        '1d in seconds'                         : lambda r: r == '86400.0',
        '1d'                                    : lambda r: r == '1 day, 0:00:00',
        '1d+0h22M'                              : lambda r: r == '1 day, 0:22:00',
        '1d1M in hours'                         : lambda r: r == '24.016666666666666',
        '1970 Jan 1 - 3h in unix'               : lambda r: int(r) <= 24*60*60,
        '1w'                                    : lambda r: r == '7 days, 0:00:00',
        '22h:22'                                : lambda r: r == '22:22:00',
        '22:22:22'                              : lambda r: r == '22:22:22',
        '22h:22M:22'                            : lambda r: r == '22:22:22',
        '22h:22:22'                             : lambda r: r == '22:22:22',
        '22h:22M:22s'                           : lambda r: r == '22:22:22',
        '22:22M:22s'                            : lambda r: r == '22:22:22',
        '22:22:22s'                             : lambda r: r == '22:22:22',
        '22h:22:22s'                            : lambda r: r == '22:22:22',
        '22:22:22s'                             : lambda r: r == '22:22:22',
        '22M:22 + 4h'                           : lambda r: r == '8:22:22',
        '2018 Jan 28 + 3y > 2021 Jan 26'        : lambda r: eval(r),
        '2 < 1'                                 : lambda r: not eval(r),
        '22:22:22'                              : lambda r: re.match(HMS_FORMAT, r),
        '22h+2M'                                : lambda r: r == '22:02:00', 
        '22h22M'                                : lambda r: r == '22:22:00', 
        '6y5m4d3h2M1s'                          : lambda r: '2346 days, 3:02:00' in r,
        '7y6m5w4d3h2M1s'                        : lambda r: '2776 days, 3:02:00' in r,
        '2h2M'                                  : lambda r: r == '2:02:00',
        '3h+3m'                                 : lambda r: r.startswith('90 days, 2:59:59'), 
        '3m'                                    : lambda r: r.startswith('89 days, 23:59:59'),
        'T-1.5d'                                : lambda r: re.match(ISO_FORMAT, r),
        'T-10d'                                 : lambda r: re.match(YMD_FORMAT, r),
        'T.day'                                 : lambda r: 0 < int(r) < 32,
        'T.dow'                                 : lambda r: r in days,
        'YD.day'                                : lambda r: re.match(r'\d+', r),
        'n'                                     : lambda r: re.match(ISO_FORMAT, r),
        'next Sunday'                           : lambda r: re.match(YMD_FORMAT, r),
        'wait .001s'                            : lambda r: len(r) == 0,
        'weekday 0'                             : lambda r: 'Wednesday',
        'yd-5h'                                 : lambda r: re.match(ISO_FORMAT, r),
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
