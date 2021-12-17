# Date Time Expression

![PyPI](https://img.shields.io/pypi/v/dte)
![Travis (.com)](https://img.shields.io/travis/com/mvrozanti/dte)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dte)
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-orange.svg)](http://www.wtfpl.net/about/)

`dte` is a WIP date-time processing language with focus on broad interpretation.

If you don't think it's intuitive, it's most likely unfinished.

It is strongly inspired by [pdd](https://github.com/jarun/pdd).

![demo](https://i.imgur.com/S7HfZZN.gif)

## How to use & What to know

`pip install dte`

### Conventions
![relevant xkcd](https://sslimgs.xkcd.com/comics/iso_8601.png)
- When there is margin for ambiguity, expressions are always interpreted with [highest units appearing before, complying with ISO-8601](https://preview.redd.it/2vjzrsib7ci61.png?width=2800&format=png&auto=webp&s=944b5176432419338cb2b13aeac10e61da1221f9), e.g.: `2021-06-13`, `2023 August 27` or `2019 Jul 20`
- Unix timestamps are both interpreted and output in seconds by default, but this is configurable
- When specifying time, just remember that `M` is for month and `m` is for minute

## Configuration File

`dte` tries to read a `config.json` file under config directory (`~/.config/dte/` on Linux). In it you can set the following options:

```
{
  "timestamp_unit": "<seconds|milliseconds>"
  "clock": "<24|12>",
  "datetime_output_format": "<ISO8601|<format>>",
  "comparison_tolerance_seconds": <float>,
  "basedate_output_format": "%Y-%b",
  "decimal_places": <integer>
}
```

### Dependencies
- [dateutil](https://github.com/dateutil/dateutil) handles month and year's complex operations
- [ply](https://github.com/dabeaz/ply) is a pure-Python implementation of the popular compiler construction tools lex and yacc 
- [appdirs](https://github.com/ActiveState/appdirs) for reading config file in a cross-platform manner

## To do
- [ ] format(timepoint, fmt) (in keyword) units given current time field
- [ ] add custom/OS locale support (?)
- [ ] add tab-completion for:
  - [ ] months
  - [ ] units given current datetime field or RHS of `in` keyword
- [ ] "days until winter"
- [ ] run tests across a variety of locales
- [ ] add `show` function
  - [ ] show clock for time
  - [ ] show cal for date and basedate

# Examples
The following examples are generated based on tests run, so many results will be relative to the day it was tested. Every expression on the left side is valid syntax.

[//]: <> (BEGIN EXAMPLES)

|INPUT| OUTPUT |
|-----|--------|
|`jan 1 + 99999M`|`8334-04-01`|
|`1970 january 1st`|`1970-01-01`|
|`day 13 friday in 2021`|`2021-08-13`|
|`friday day < 8 in Jan 2015`|`2015-01-02`|
|`friday day 13 in August 2021.weekday`|`Friday`|
|`friday day 13 in August 2021`|`2021-08-13`|
|`2020-01-29 + (1 year + 1 month)`|`2021-02-28`|
|`days until Jan 2030`|`2936.18`|
|`last sun in 2021`|`2021-12-26`|
|`april+1M`|`2022-05-01`|
|`t+1d 08h30`|`2021-12-18 08:30:00`|
|`1am t == t 1am`|`True`|
|`1am t`|`2021-12-17 01:00:00`|
|`(2020-10-10+1d) 3pm`|`2020-10-11 15:00:00`|
|`t 1:00 == t 1am`|`True`|
|`t 1:00`|`2021-12-17 01:00:00`|
|`t 1am`|`2021-12-17 01:00:00`|
|`august`|`2021-Aug`|
|`4th wed in august`|`2021-08-25`|
|`5th sunday in 2021`|`2021-01-31`|
|`4th sunday in 2021`|`2021-01-24`|
|`3rd sunday in 2021`|`2021-01-17`|
|`2nd sunday in 2021`|`2021-01-10`|
|`-1d + 2020-10-10`|`2020-10-09`|
|`2014 Jan + 1M`|`2014-02-01`|
|`Jan 2014 + 1M`|`2014-02-01`|
|`seconds in 24h`|`86400.00`|
|`today==mon`|`False`|
|`days until mon`|`2.18`|
|`days until next mon`|`2.18`|
|`next mon + 1d`|`2021-12-21`|
|`monday+1d`|`2021-12-21`|
|`weekday t+100d`|`Sunday`|
|`(weekday t+100d)==100d.weekday`|`True`|
|`(weekday t+100d)`|`Sunday`|
|`weekday tm`|`Saturday`|
|`yesterday==thu`|`True`|
|`yesterday==thursday`|`True`|
|`last fri in Dec 2014`|`2014-12-26`|
|`last fri in 2014 Dec`|`2014-12-26`|
|`last fri in 2014 December`|`2014-12-26`|
|`days until 2030-12-25`|`3294.18`|
|`6pm+1h`|`19:00:00`|
|`2014 01`|`2014-Jan`|
|`1st friday in april`|`2022-04-01`|
|`first friday in april`|`2022-04-01`|
|`1st friday in next month`|`2022-01-07`|
|`first friday in next month`|`2022-01-07`|
|`next month`|`2022-01-01`|
|`seconds until 11 pm`|`11736.53`|
|`seconds until tomorrow`|`15336.45`|
|`1996 August 28 9 AM`|`1996-08-28 09:00:00`|
|`2s2s`|`0:00:04`|
|`1 hour in seconds`|`3600.00`|
|`1h in seconds`|`3600.00`|
|`5m+5m`|`0:10:00`|
|`1957-12-26 22:22:22 in unix`|`-379118258`|
|`yd-5h`|`2021-12-15 19:00:00`|
|`1st sun in April 2021`|`2021-04-04`|
|`first sun in April 2021`|`2021-04-04`|
|`1st friday in April 2014`|`2014-04-04`|
|`first friday in April 2014`|`2014-04-04`|
|`Jan 2014`|`2014-Jan`|
|`weekday 0`|`Wednesday`|
|`wait until (n+.001s)`|``|
|`wait .001s`|``|
|`t - next Sunday`|`-2 days, 0:00:00`|
|`2012-12-13-3y.weekday`|`Sunday`|
|`1st sunday in 2021`|`2021-01-03`|
|`first sunday in 2021`|`2021-01-03`|
|`last sunday in 2021`|`2021-12-26`|
|`last Sunday != next sunday`|`True`|
|`last Sunday == next sunday`|`False`|
|`next Sunday != last sunday`|`True`|
|`next Sunday == last sunday`|`False`|
|`seconds since 3000 Apr 10`|`-30872463334.53`|
|`seconds until 3000 Apr 10`|`30872463334.45`|
|`2000-10-10 16:00`|`2000-10-10 16:00:00`|
|`2000-10-10 00:16`|`2000-10-10 00:16:00`|
|`next Sunday`|`2021-12-19`|
|`n`|`2021-12-17 19:44:25.868383`|
|`YD.day`|`16`|
|`T.weekday`|`Friday`|
|`T.day`|`17`|
|`T-10d`|`2021-12-07`|
|`T-1.5d`|`2021-12-15 12:00:00`|
|`3M`|`3 months`|
|`3h+3M`|`3 months, 3:00:00`|
|`2h2m`|`2:02:00`|
|`7y6M5w4d3h2m1.1s`|`7 years, 6 months, 39 days, 3:02:01`|
|`1M1d`|`1 month, 1 day, 0:00:00`|
|`-1y2M`|`-1 year, -2 months`|
|`0y2M`|`2 months`|
|`1y2M`|`1 year, 2 months`|
|`6y5M4d3h2m1s`|`6 years, 5 months, 4 days, 3:02:01`|
|`22h22m`|`22:22:00`|
|`22h+2m`|`22:02:00`|
|`12h:00 pm != 12h:00 am`|`True`|
|`2 < 1`|`False`|
|`2020 Jan 27 + 1y == 2021 Jan 27`|`True`|
|`1w`|`7 days, 0:00:00`|
|`1970 Jan 1 - 3h in unix`|`0`|
|`1d1m in hours`|`24.02`|
|`1d+0h22m`|`1 day, 0:22:00`|
|`1d`|`1 day, 0:00:00`|
|`1d in seconds`|`86400.00`|
|`1d in minutes`|`1440.00`|
|`1d in hours`|`24.00`|
|`1958-05-14 - 1958-05-16`|`-2 days, 0:00:00`|
|`1957-12-26 22:22:22 - t`|`-23367 days, 22:22:22`|
|`1957-12-26 - t`|`-23367 days, 0:00:00`|
|`2014 Jan 13==2014 January 13`|`True`|
|`12h:00 AM != 12h:00 PM`|`True`|
|`1610494238.weekday`|`Tuesday`|
|`1610494238+4h.weekday`|`Wednesday`|
|`1610494238`|`2021-01-12 20:30:38`|
|`1-1-1-1-1-1`|`0:00:00`|
|`22m:22 + 4h`|`4:22:22`|
|`6pm`|`18:00:00`|
|`6 pm + 1h`|`19:00:00`|
|`6 pm`|`18:00:00`|
|`2020-Jan-27`|`2020-01-27`|
|`22:22:22`|`22:22:22`|
|`22:22:22s`|`22:22:22`|
|`22h:22:22s`|`22:22:22`|
|`22:22m:22s`|`22:22:22`|
|`22h:22m:22s`|`22:22:22`|
|`22h:22m:22`|`22:22:22`|
|`22h:22`|`22:22:00`|
|`1996.04.28`|`1996-04-28`|
|`2014 January 13`|`2014-01-13`|
|`2014 Jan 13`|`2014-01-13`|
|`11:20s PM`|`00:11:20`|
|`11h:20m pm`|`23:20:00`|
|`11h:20 am`|`11:20:00`|
|`11m:20 PM`|`00:11:20`|
|`11h:20 AM`|`11:20:00`|
|`1-1-1 23:23S`|`0001-01-01 00:23:23`|
|`1-1-1 23m:23S`|`0001-01-01 00:23:23`|
|`1-1-1 23m:23s`|`0001-01-01 00:23:23`|
|`1-1-1 23m:23`|`0001-01-01 00:23:23`|
|`1-1-1 23h:23m`|`0001-01-01 23:23:00`|
|`1-1-1 23h:23`|`0001-01-01 23:23:00`|
|`1-1-1 23:23m`|`0001-01-01 23:23:00`|
|`1-1-1 23:23:23`|`0001-01-01 23:23:23`|
|`seconds until 2021 feb 14 12:00:00`|`-26466270.99`|
|`2021 feb 14 12:00:00`|`2021-02-14 12:00:00`|
|`10h30 + 14h`|`1 day, 0:30:00`|
|`n - 1234`|`18978 days, 22:23:57.238947`|
|`1m in hours`|`0.02`|
|`1 in unix`|`1`|
|`08h30`|`8:30:00`|
|`-1d.weekday`|`Thursday`|
|`(t + 180d)-180d == t`|`True`|
|`(n + 181d)-180d != n`|`True`|
|`(n + 180d)-180d == n`|`True`|
|`(T-1d).weekday`|`Thursday`|
