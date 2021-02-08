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

DELTA_FORMAT = r'-?\d+ days?, \d{1,2}:\d{2}:\d{2}'

test_expectancy = {
        '(T-1d).dow'                            : lambda r: r in days,
        '(n + 180d)-180d == n'                  : lambda r: eval(r),
        '(n + 181d)-180d != n'                  : lambda r: eval(r),
        '(t + 180d)-180d == t'                  : lambda r: eval(r),
        '-1d.dow'                               : lambda r: r in days,
        '08h30'                                 : lambda r: r == '8:30:00',
        '1 in unix'                             : lambda r: r == '1',
        'n - 1234'                              : lambda r: re.match(DELTA_FORMAT, r),
        '10h30 + 14h'                           : lambda r: r == '1 day, 0:30:00',
        '2021 feb 14 12:00:00'                  : lambda r: r == '2021-02-14 12:00:00',
        'seconds until 2021 feb 14 12:00:00'    : lambda r: float(r) < 580301.752936,
        '1-1-1 23:23:23'                        : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23:23m'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23h:23'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23h:23m'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23m:23'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23m:23s'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23m:23S'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23:23S'                          : lambda r: re.match(ISO_FORMAT, r),
        '11h:20 AM'                             : lambda r: r == '11:20:00',
        '11m:20 PM'                             : lambda r: r == '00:11:20',
        '11h:20 am'                             : lambda r: r == '11:20:00',
        '11h:20M pm'                            : lambda r: r == '23:20:00',
        '11:20s PM'                             : lambda r: r == '00:11:20',
        '2014 Jan 13'                           : lambda r: r == '2014-01-13',
        '2014 January 13'                       : lambda r: r == '2014-01-13',
        '1996.04.28'                            : lambda r: r == '1996-04-28',
        '22h:22'                                : lambda r: r == '22:22:00',
        '22:22:22'                              : lambda r: r == '22:22:22',
        '22h:22m:22'                            : lambda r: r == '22:22:22',
        '22h:22m:22s'                           : lambda r: r == '22:22:22',
        '22:22m:22s'                            : lambda r: r == '22:22:22',
        '22h:22:22s'                            : lambda r: r == '22:22:22',
        '22:22:22s'                             : lambda r: r == '22:22:22',
        '22:22:22'                              : lambda r: re.match(HMS_FORMAT, r),
        '2020-Jan-27'                           : lambda r: r == '2020-01-27',
        '6 pm'                                  : lambda r: re.match(HMS_FORMAT, r),
        '6 pm + 1h'                             : lambda r: re.match(HMS_FORMAT, r),
        '22m:22 + 4h'                           : lambda r: r == '4:22:22',
        '1-1-1-1-1-1'                           : lambda r: re.match(HMS_FORMAT, r),
        '1610494238'                            : lambda r: '2021-01-12' in r,
        '1610494238+4h.dow'                     : lambda r: r == 'Wednesday',
        '1610494238.dow'                        : lambda r: r == 'Tuesday',
        '12h:00 AM != 12h:00 PM'                : lambda r: eval(r),
        '2014 Jan 13==2014 January 13'          : lambda r: eval(r),
        'help'                                  : lambda r: len(r) > 1500,
        '1957-12-26 - t'                        : lambda r: re.match(DELTA_FORMAT, r),
        '1957-12-26 22:22:22 - t'               : lambda r: re.match(DELTA_FORMAT, r),
        '1958-05-14 - 1958-05-16'               : lambda r: r == '-2 days, 0:00:00',
        '1d in hours'                           : lambda r: r == '24.0',
        '1d in minutes'                         : lambda r: r == '1440.0',
        '1d in seconds'                         : lambda r: r == '86400.0',
        '1d'                                    : lambda r: r == '1 day, 0:00:00',
        '1d+0h22m'                              : lambda r: r == '1 day, 0:22:00',
        '1d1m in hours'                         : lambda r: r == '24.016666666666666',
        '1970 Jan 1 - 3h in unix'               : lambda r: int(r) <= 24*60*60,
        '1w'                                    : lambda r: r == '7 days, 0:00:00',
        '2020 Jan 27 + 1y == 2021 Jan 26'       : lambda r: eval(r),
        '2 < 1'                                 : lambda r: not eval(r),
        '12h:00 pm != 12h:00 am'                : lambda r: eval(r),
        '22h+2m'                                : lambda r: r == '22:02:00', 
        '22h22m'                                : lambda r: r == '22:22:00', 
        '6y5M4d3h2m1s'                          : lambda r: re.match(r'234\d days, 3:02:.*', r),
        '7y6M5w4d3h2m1.1s'                      : lambda r: r.startswith('2776 days, 3:02:01'),
        '2h2m'                                  : lambda r: r == '2:02:00',
        '3h+3M'                                 : lambda r: re.match('[89][90] days, 2:59:59.*', r),
        '3M'                                    : lambda r: re.match('[89][890] days, 23:59:59.*', r),
        'T-1.5d'                                : lambda r: re.match(ISO_FORMAT, r),
        'T-10d'                                 : lambda r: re.match(YMD_FORMAT, r),
        'T.day'                                 : lambda r: 0 < int(r) < 32,
        'T.dow'                                 : lambda r: r in days,
        'YD.day'                                : lambda r: re.match(r'\d+', r),
        'n'                                     : lambda r: re.match(ISO_FORMAT, r),
        'next Sunday'                           : lambda r: re.match(YMD_FORMAT, r),
        'seconds until 3000 Apr 10'             : lambda r: 30899416627.60163 > float(r),
        'seconds since 3000 Apr 10'             : lambda r: -30899416627.60163 < float(r),
        'next Sunday != last sunday'            : lambda r: eval(r),
        'last sunday in 2021'                   : lambda r: r == '2021-12-26',
        'first sunday in 2021'                  : lambda r: r == '2021-01-03',
        't - next Sunday'                       : lambda r: re.match(DELTA_FORMAT, r),
        'wait .001s'                            : lambda r: len(r) == 0,
        'weekday 0'                             : lambda r: 'Wednesday',
        'yd-5h'                                 : lambda r: re.match(ISO_FORMAT, r),
        '1957-12-26 22:22:22 in unix'           : lambda r: -379118258 - 86400 < int(r) < -379118258 + 86400,
        }

class Tester(unittest.TestCase):

    def test_stuff(self):
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
