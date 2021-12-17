#!/usr/bin/env -S python -m pytest
from collections import OrderedDict
from subprocess import Popen, PIPE, call
import code  # noqa
import os
from os import path as op
import re
import unittest

days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']

ISO_FORMAT = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?$'

YMD_FORMAT = r'^\d{4}-\d{2}-\d{2}$'

YMD_LIST_FORMAT = r'(\d{4}-\d{2}-\d{2}|\n)*'

DAY_LIST_FORMAT = r'(' + '|'.join(days) + '|\n)*'

HMS_FORMAT = r'^\d+:\d+:\d+$'

DELTA_FORMAT = r'(-?\d+ years?, (-?\d+ months?(, )?)? ?)?(-?\d+ days?, \d{1,2}:\d{2}:\d{2})?'

BASEDATE_FORMAT = r'\d+-\w+'

test_expectancy = OrderedDict({
        # 'days since easter'                 : lambda
        # 'days until easter'                 : lambda
        # 'easter 2014'                       : lambda
        # 'fridays in 2015' # rrule
        # 'fris in 2015' # rrule
        # 'friday day = 8 in Jan 2015' : lambda r: r == '2015-01-02',

        # '2014 Jan 3:00'                         : lambda r: False,
        # 'Jan 2014 3:00'                         : lambda r: False,
        'jan 1 + 99999M'                        : lambda r: r.endswith('01'),
        '1970 january 1st'                      : lambda r: re.match(YMD_LIST_FORMAT, r), 
        'day 13 friday in 2021'                 : lambda r: re.match(YMD_LIST_FORMAT, r),
        'friday day < 13 in 2014 sep'           : lambda r: re.match(YMD_LIST_FORMAT, r),
        'friday in Jan 2015'                    : lambda r: re.match(YMD_LIST_FORMAT, r),
        'friday day < 8 in Jan 2015'            : lambda r: r == '2015-01-02',
        'friday day > 8 in Jan 2015 to Jan 2019': lambda r: re.match(YMD_LIST_FORMAT, r),
        'friday day < 8 in Jan 2015 to Jan 2019': lambda r: re.match(YMD_LIST_FORMAT, r),
        'friday day 13 in Jan 2015 to Jan 2019' : lambda r: re.match(YMD_LIST_FORMAT, r),
        'friday day 13 in August 2021.weekday'  : lambda r: r == 'Friday',
        'friday day 13 in August 2021'          : lambda r: r == '2021-08-13',
        'friday day 13 in 2015.weekday'         : lambda r: re.match(DAY_LIST_FORMAT, r),
        'friday day 13 in 2015'                 : lambda r: re.match(YMD_LIST_FORMAT, r),
        'fri in 2015'                           : lambda r: re.match(YMD_LIST_FORMAT, r),
        'friday in 2015'                        : lambda r: re.match(YMD_LIST_FORMAT, r),
        '2020-01-29 + (1 year + 1 month)'       : lambda r: r == '2021-02-28',
        'days until Jan 2030'                   : lambda r: float(r) < 3002,
        'last sun in 2021'                      : lambda r: r == '2021-12-26',
        'april+1M'                              : lambda r: re.match(YMD_FORMAT, r),
        't+1d 08h30'                            : lambda r: re.match(ISO_FORMAT, r),
        '1am t == t 1am'                        : lambda r: eval(r),
        '1am t'                                 : lambda r: re.match(ISO_FORMAT, r),
        '(2020-10-10+1d) 3pm'                   : lambda r: '2020-10-11 15:00:00' == r, 
        't 1:00 == t 1am'                       : lambda r: eval(r),
        't 1:00'                                : lambda r: re.match(ISO_FORMAT, r),
        't 1am'                                 : lambda r: re.match(ISO_FORMAT, r),
        'august'                                : lambda r: re.match(BASEDATE_FORMAT, r),
        '4th wed in august'                     : lambda r: re.match(YMD_FORMAT, r),
        '5th sunday in 2021'                    : lambda r: r == '2021-01-31',
        '4th sunday in 2021'                    : lambda r: r == '2021-01-24',
        '3rd sunday in 2021'                    : lambda r: r == '2021-01-17',
        '2nd sunday in 2021'                    : lambda r: r == '2021-01-10',
        '-1d + 2020-10-10'                      : lambda r: r == '2020-10-09',
        '2014 Jan + 1M'                         : lambda r: re.match(YMD_FORMAT, r),
        'Jan 2014 + 1M'                         : lambda r: re.match(YMD_FORMAT, r),
        'seconds in 24h'                        : lambda r: float(r) == 86400,
        'today==mon'                            : lambda r: r in ['True', 'False'],
        'days until mon'                        : lambda r: -4.5 < float(r) < 4.5,
        'days until next mon'                   : lambda r: 0 <= float(r) <= 7,
        'next mon + 1d'                         : lambda r: re.match(YMD_FORMAT, r),
        'monday+1d'                             : lambda r: re.match(YMD_FORMAT, r),
        'weekday t+100d'                        : lambda r: r in days,
        '(weekday t+100d)==100d.weekday'        : lambda r: eval(r),
        '(weekday t+100d)'                      : lambda r: r in days,
        'weekday tm'                            : lambda r: r in days,
        'yesterday==thu'                        : lambda r: r in ['True', 'False'],
        'yesterday==thursday'                   : lambda r: r in ['True', 'False'],
        'last fri in Dec 2014'                  : lambda r: re.match(YMD_FORMAT, r),
        'last fri in 2014 Dec'                  : lambda r: re.match(YMD_FORMAT, r),
        'last fri in 2014 December'             : lambda r: re.match(YMD_FORMAT, r),
        'days until 2030-12-25'                 : lambda r: float(r) < 3364.55,
        '6pm+1h'                                : lambda r: re.match(HMS_FORMAT, r),
        '2014 01'                               : lambda r: re.match(BASEDATE_FORMAT, r), 
        '1st friday in april'                   : lambda r: re.match(YMD_FORMAT, r) and r.split('-')[1] == '04',
        'first friday in april'                 : lambda r: re.match(YMD_FORMAT, r) and r.split('-')[1] == '04',
        '1st friday in next month'              : lambda r: re.match(YMD_FORMAT, r),
        'first friday in next month'            : lambda r: re.match(YMD_FORMAT, r),
        'next month'                            : lambda r: re.match(BASEDATE_FORMAT, r),
        'seconds until 11 pm'                   : lambda r: float(r) < 86400,
        'seconds until tomorrow'                : lambda r: 0 < float(r) < 86400,
        '1996 August 28 9 AM'                   : lambda r: r == '1996-08-28 09:00:00',
        '2s2s'                                  : lambda r: r == '0:00:04',
        '1 hour in seconds'                     : lambda r: r == '3600.00',
        '1h in seconds'                         : lambda r: r == '3600.00',
        '5m+5m'                                 : lambda r: r == '0:10:00',
        '1957-12-26 22:22:22 in unix'           : lambda r: -379118258 - 86400 < int(r) < -379118258 + 86400,
        'yd-5h'                                 : lambda r: re.match(ISO_FORMAT, r),
        '1st sun in April 2021'                 : lambda r: r == '2021-04-04',
        'first sun in April 2021'               : lambda r: r == '2021-04-04',
        '1st friday in April 2014'              : lambda r: r == '2014-04-04',
        'first friday in April 2014'            : lambda r: r == '2014-04-04',
        'Jan 2014'                              : lambda r: re.match(BASEDATE_FORMAT, r),
        'weekday 0'                             : lambda r: r in ['Wednesday', 'Thursday'],
        'wait until (n+.001s)'                  : lambda r: len(r) == 0,
        'wait .001s'                            : lambda r: len(r) == 0,
        't - next Sunday'                       : lambda r: re.match(DELTA_FORMAT, r),
        '2012-12-13-3y.weekday'                 : lambda r: r == 'Sunday',
        '1st sunday in 2021'                    : lambda r: r == '2021-01-03',
        'first sunday in 2021'                  : lambda r: r == '2021-01-03',
        'last sunday in 2021'                   : lambda r: r == '2021-12-26',
        'last Sunday != next sunday'            : lambda r: r == 'True',
        'last Sunday == next sunday'            : lambda r: r == 'False',
        'next Sunday != last sunday'            : lambda r: r == 'True',
        'next Sunday == last sunday'            : lambda r: r == 'False',
        'seconds since 3000 Apr 10'             : lambda r: -30899416627.60163 < float(r),
        'seconds until 3000 Apr 10'             : lambda r: 30899416627.60163 > float(r),
        '2000-10-10 16:00'                      : lambda r: r == '2000-10-10 16:00:00',
        '2000-10-10 00:16'                      : lambda r: r == '2000-10-10 00:16:00',
        'next Sunday'                           : lambda r: re.match(YMD_FORMAT, r),
        'n'                                     : lambda r: re.match(ISO_FORMAT, r),
        'YD.day'                                : lambda r: re.match(r'\d+', r),
        'T.weekday'                             : lambda r: r in days,
        'T.day'                                 : lambda r: 0 < int(r) < 32,
        'T-10d'                                 : lambda r: re.match(YMD_FORMAT, r),
        'T-1.5d'                                : lambda r: re.match(ISO_FORMAT, r),
        '3M'                                    : lambda r: re.match(DELTA_FORMAT, r),
        '3h+3M'                                 : lambda r: re.match(DELTA_FORMAT, r),
        '2h2m'                                  : lambda r: r == '2:02:00',
        '7y6M5w4d3h2m1.1s'                      : lambda r: re.match(DELTA_FORMAT, r),
        '1M1d'                                  : lambda r: r == '1 month, 1 day, 0:00:00',
        '-1y2M'                                 : lambda r: re.match(DELTA_FORMAT, r),
        '0y2M'                                  : lambda r: r == '2 months',
        '1y2M'                                  : lambda r: r == '1 year, 2 months',
        '6y5M4d3h2m1s'                          : lambda r: re.match(DELTA_FORMAT, r),
        '22h22m'                                : lambda r: r == '22:22:00', 
        '22h+2m'                                : lambda r: r == '22:02:00', 
        '12h:00 pm != 12h:00 am'                : lambda r: eval(r),
        '2 < 1'                                 : lambda r: not eval(r),
        '2020 Jan 27 + 1y == 2021 Jan 27'       : lambda r: eval(r),
        '1w'                                    : lambda r: r == '7 days, 0:00:00',
        '1970 Jan 1 - 3h in unix'               : lambda r: int(r) <= 24*60*60,
        '1d1m in hours'                         : lambda r: r == '24.02',
        '1d+0h22m'                              : lambda r: r == '1 day, 0:22:00',
        '1d'                                    : lambda r: r == '1 day, 0:00:00',
        '1d in seconds'                         : lambda r: r == '86400.00',
        '1d in minutes'                         : lambda r: r == '1440.00',
        '1d in hours'                           : lambda r: r == '24.00',
        '1958-05-14 - 1958-05-16'               : lambda r: r == '-2 days, 0:00:00',
        '1957-12-26 22:22:22 - t'               : lambda r: re.match(DELTA_FORMAT, r),
        '1957-12-26 - t'                        : lambda r: re.match(DELTA_FORMAT, r),
        '2014 Jan 13==2014 January 13'          : lambda r: eval(r),
        '12h:00 AM != 12h:00 PM'                : lambda r: eval(r),
        '1610494238.weekday'                    : lambda r: r == 'Tuesday',
        '1610494238+4h.weekday'                 : lambda r: r == 'Wednesday',
        '1610494238'                            : lambda r: '2021-01-12' in r,
        '1-1-1-1-1-1'                           : lambda r: '0:00:00',
        '22m:22 + 4h'                           : lambda r: r == '4:22:22',
        '6pm'                                   : lambda r: re.match(HMS_FORMAT, r),
        '6 pm + 1h'                             : lambda r: re.match(HMS_FORMAT, r),
        '6 pm'                                  : lambda r: re.match(HMS_FORMAT, r),
        '2020-Jan-27'                           : lambda r: r == '2020-01-27',
        '22:22:22'                              : lambda r: re.match(HMS_FORMAT, r),
        '22:22:22s'                             : lambda r: r == '22:22:22',
        '22h:22:22s'                            : lambda r: r == '22:22:22',
        '22:22m:22s'                            : lambda r: r == '22:22:22',
        '22h:22m:22s'                           : lambda r: r == '22:22:22',
        '22h:22m:22'                            : lambda r: r == '22:22:22',
        '22:22:22'                              : lambda r: r == '22:22:22',
        '22h:22'                                : lambda r: r == '22:22:00',
        '1996.04.28'                            : lambda r: r == '1996-04-28',
        '2014 January 13'                       : lambda r: r == '2014-01-13',
        '2014 Jan 13'                           : lambda r: r == '2014-01-13',
        '11:20s PM'                             : lambda r: r == '00:11:20',
        '11h:20m pm'                            : lambda r: r == '23:20:00',
        '11h:20 am'                             : lambda r: r == '11:20:00',
        '11m:20 PM'                             : lambda r: r == '00:11:20',
        '11h:20 AM'                             : lambda r: r == '11:20:00',
        '1-1-1 23:23S'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23m:23S'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23m:23s'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23m:23'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23h:23m'                         : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23h:23'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23:23m'                          : lambda r: re.match(ISO_FORMAT, r),
        '1-1-1 23:23:23'                        : lambda r: re.match(ISO_FORMAT, r),
        'seconds until 2021 feb 14 12:00:00'    : lambda r: float(r) < 580301.752936,
        '2021 feb 14 12:00:00'                  : lambda r: r == '2021-02-14 12:00:00',
        '10h30 + 14h'                           : lambda r: r == '1 day, 0:30:00',
        'n - 1234'                              : lambda r: re.match(DELTA_FORMAT, r),
        '1m in hours'                           : lambda r: r == '0.02',
        '1 in unix'                             : lambda r: r == '1',
        '08h30'                                 : lambda r: r == '8:30:00',
        '-1d.weekday'                           : lambda r: r in days,
        '(t + 180d)-180d == t'                  : lambda r: eval(r),
        '(n + 181d)-180d != n'                  : lambda r: eval(r),
        '(n + 180d)-180d == n'                  : lambda r: eval(r),
        '(T-1d).weekday'                        : lambda r: r in days,
        })


def run(test):
    dte_location = os.path.dirname(os.path.realpath(__file__)) \
                             + op.sep + '..' \
                             + (op.sep + 'dte')*2
    p = Popen(dte_location, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(test.encode('utf-8'))
    out = out.decode('utf-8').replace('\n', '')
    return out, err


def make_documentation(test_out):
    import pathlib
    le_path = pathlib.Path(__file__).parent.resolve()
    call(['sed', '-i', '/BEGIN EXAMPLES/q', f'{le_path}/../README.md'])
    with open('../README.md', 'a') as f:
        f.write('\n|INPUT| OUTPUT |\n')
        f.write('|-----|--------|\n')
        for test, out in test_out.items():
            if '\r' not in out:
                f.write('|`' + test + '`|`' + out + '`|\n')


class Tester(unittest.TestCase):

    def test_stuff(self):
        test_out = OrderedDict()
        for test, expectancy in test_expectancy.items():
            try:
                out, err = run(test)
                test_out[test] = out
                assert expectancy(out) and not err
            except Exception as e:
                print(test)
                raise e
        make_documentation(test_out)
