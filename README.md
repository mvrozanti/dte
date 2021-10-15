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
`(T-1d).weekday` returns `Thursday`

`(n + 180d)-180d == n` returns `True`

`(n + 181d)-180d != n` returns `True`

`(t + 180d)-180d == t` returns `True`

`-1d.weekday` returns `Thursday`

`08h30` returns `8:30:00`

`1 in unix` returns `1`

`n - 1234` returns `18915 days, 17:59:59.240107`

`10h30 + 14h` returns `1 day, 0:30:00`

`2021 feb 14 12:00:00` returns `2021-02-14 12:00:00`

`seconds until 2021 feb 14 12:00:00` returns `-21007233.48`

`1-1-1 23:23:23` returns `0001-01-01 23:23:23`

`1-1-1 23:23m` returns `0001-01-01 23:23:00`

`1-1-1 23h:23` returns `0001-01-01 23:23:00`

`1-1-1 23h:23m` returns `0001-01-01 23:23:00`

`1-1-1 23m:23` returns `0001-01-01 00:23:23`

`1-1-1 23m:23s` returns `0001-01-01 00:23:23`

`1-1-1 23m:23S` returns `0001-01-01 00:23:23`

`1-1-1 23:23S` returns `0001-01-01 00:23:23`

`11h:20 AM` returns `11:20:00`

`11m:20 PM` returns `00:11:20`

`11h:20 am` returns `11:20:00`

`11h:20m pm` returns `23:20:00`

`11:20s PM` returns `00:11:20`

`2014 Jan 13` returns `2014-01-13`

`2014 January 13` returns `2014-01-13`

`1996.04.28` returns `1996-04-28`

`22h:22` returns `22:22:00`

`22:22:22` returns `22:22:22`

`22h:22m:22` returns `22:22:22`

`22h:22m:22s` returns `22:22:22`

`22:22m:22s` returns `22:22:22`

`22h:22:22s` returns `22:22:22`

`22:22:22s` returns `22:22:22`

`2020-Jan-27` returns `2020-01-27`

`6 pm` returns `18:00:00`

`6 pm + 1h` returns `19:00:00`

`6pm` returns `18:00:00`

`22m:22 + 4h` returns `4:22:22`

`1-1-1-1-1-1` returns `0:00:00`

`1610494238` returns `2021-01-12 20:30:38`

`1610494238+4h.weekday` returns `Wednesday`

`1610494238.weekday` returns `Tuesday`

`12h:00 AM != 12h:00 PM` returns `True`

`2014 Jan 13==2014 January 13` returns `True`

`1957-12-26 - t` returns `-23304 days, 0:00:00`

`1957-12-26 22:22:22 - t` returns `-23304 days, 22:22:22`

`1958-05-14 - 1958-05-16` returns `-2 days, 0:00:00`

`1d in hours` returns `24.00`

`1d in minutes` returns `1440.00`

`1d in seconds` returns `86400.00`

`1d` returns `1 day, 0:00:00`

`1d+0h22m` returns `1 day, 0:22:00`

`1d1m in hours` returns `24.02`

`1970 Jan 1 - 3h in unix` returns `0`

`1w` returns `7 days, 0:00:00`

`2020 Jan 27 + 1y == 2021 Jan 26` returns `True`

`2 < 1` returns `False`

`12h:00 pm != 12h:00 am` returns `True`

`22h+2m` returns `22:02:00`

`22h22m` returns `22:22:00`

`6y5M4d3h2m1s` returns `2346 days, 3:02:01`

`7y6M5w4d3h2m1.1s` returns `2778 days, 3:02:01.100000`

`2h2m` returns `2:02:00`

`3h+3M` returns `92 days, 3:00:00`

`3M` returns `92 days, 0:00:00`

`T-1.5d` returns `2021-10-13 12:00:00`

`T-10d` returns `2021-10-05`

`T.day` returns `15`

`T.weekday` returns `Friday`

`YD.day` returns `14`

`n` returns `2021-10-15 15:20:38.280013`

`next Sunday` returns `2021-10-17`

`2000-10-10 00:16` returns `2000-10-10 00:16:00`

`2000-10-10 16:00` returns `2000-10-10 16:00:00`

`seconds until 3000 Apr 10` returns `30877922361.42`

`seconds since 3000 Apr 10` returns `-30877922361.34`

`next Sunday == last sunday` returns `False`

`next Sunday != last sunday` returns `True`

`last Sunday == next sunday` returns `False`

`last Sunday != next sunday` returns `True`

`last sunday in 2021` returns `2021-12-26`

`first sunday in 2021` returns `2021-01-03`

`1st sunday in 2021` returns `2021-01-03`

`2012-12-13-3y.weekday` returns `Sunday`

`t - next Sunday` returns `-2 days, 0:00:00`

`wait .001s` returns ``

`weekday 0` returns `Wednesday`

`Jan 2014` returns `2014-Jan`

`first friday in April 2014` returns `2014-04-04`

`1st friday in April 2014` returns `2014-04-04`

`first sun in April 2021` returns `2021-04-04`

`1st sun in April 2021` returns `2021-04-04`

`yd-5h` returns `2021-10-13 19:00:00`

`1957-12-26 22:22:22 in unix` returns `-379118258`

`5m+5m` returns `0:10:00`

`1h in seconds` returns `3600.00`

`1 hour in seconds` returns `3600.00`

`2s2s` returns `0:00:04`

`1996 August 28 9 AM` returns `1996-08-28 09:00:00`

`seconds until tomorrow` returns `31159.48`

`seconds until 11 pm` returns `27559.40`

`next month` returns `2021-11-01`

`first friday in next month` returns `2021-11-05`

`1st friday in next month` returns `2021-11-05`

`first friday in april` returns `2021-04-02`

`1st friday in april` returns `2021-04-02`

`2014 01` returns `2014-Jan`

`6pm+1h` returns `19:00:00`

`days until 2030-12-25` returns `3357.36`

`last fri in 2014 December` returns `2014-12-26`

`last fri in 2014 Dec` returns `2014-12-26`

`last fri in Dec 2014` returns `2014-12-26`

`yesterday==thursday` returns `True`

`yesterday==thu` returns `True`

`weekday tm` returns `Saturday`

`(weekday t+100d)` returns `Sunday`

`(weekday t+100d)==100d.weekday` returns `True`

`weekday t+100d` returns `Sunday`

`monday+1d` returns `2021-10-19`

`next mon + 1d` returns `2021-10-19`

`next mon + 1d == next tue` returns `True`

`days until next mon` returns `2.36`

`days until mon` returns `2.36`

`today==mon` returns `False`

`seconds in 24h` returns `86400.00`

`Jan 2014 + 1M` returns `2014-02-01`

`2014 Jan + 1M` returns `2014-02-01`

`-1d + 2020-10-10` returns `2020-10-09`

`2nd sunday in 2021` returns `2021-01-10`

`3rd sunday in 2021` returns `2021-01-17`

`4th sunday in 2021` returns `2021-01-24`

`5th sunday in 2021` returns `2021-01-31`

`4th wed in august` returns `2021-08-25`

`august` returns `2021-Aug`

`t 1am` returns `2021-10-15 01:00:00`

`t 1:00` returns `2021-10-15 01:00:00`

`t 1:00 == t 1am` returns `True`

`(2020-10-10+1d) 3pm` returns `2020-10-11 15:00:00`

`1am t` returns `2021-10-15 01:00:00`

`1am t == t 1am` returns `True`

`t+1d 08h30` returns `2021-10-16 08:30:00`

`april+1M` returns `2021-05-02`

`last sun in 2021` returns `2021-12-26`

`days until Jan 2030` returns `2999.36`

`2020-01-29 + (1 year + 1 month)` returns `2021-02-28`

`friday in 2015` returns ``

`fri in 2015` returns ``

`friday day 13 in 2015` returns `2015-02-132015-03-132015-11-13`

`friday day 13 in 2015.weekday` returns `FridayFridayFriday`

`friday day 13 in August 2021` returns `2021-08-13`

`friday day 13 in August 2021.weekday` returns `Friday`

`friday day 13 in Jan 2015 to Jan 2019` returns `2015-02-132015-03-132015-11-132016-05-132017-01-132017-10-132018-04-132018-07-13`

`friday day < 8 in Jan 2015 to Jan 2019` returns `2015-01-022015-02-062015-03-062015-04-032015-05-012015-06-052015-07-032015-08-072015-09-042015-10-022015-11-062015-12-042016-01-012016-02-052016-03-042016-04-012016-05-062016-06-032016-07-012016-08-052016-09-022016-10-072016-11-042016-12-022017-01-062017-02-032017-03-032017-04-072017-05-052017-06-022017-07-072017-08-042017-09-012017-10-062017-11-032017-12-012018-01-052018-02-022018-03-022018-04-062018-05-042018-06-012018-07-062018-08-032018-09-072018-10-052018-11-022018-12-07`

`friday day > 8 in Jan 2015 to Jan 2019` returns `2015-01-092015-01-162015-01-232015-01-302015-02-132015-02-202015-02-272015-03-132015-03-202015-03-272015-04-102015-04-172015-04-242015-05-152015-05-222015-05-292015-06-122015-06-192015-06-262015-07-102015-07-172015-07-242015-07-312015-08-142015-08-212015-08-282015-09-112015-09-182015-09-252015-10-092015-10-162015-10-232015-10-302015-11-132015-11-202015-11-272015-12-112015-12-182015-12-252016-01-152016-01-222016-01-292016-02-122016-02-192016-02-262016-03-112016-03-182016-03-252016-04-152016-04-222016-04-292016-05-132016-05-202016-05-272016-06-102016-06-172016-06-242016-07-152016-07-222016-07-292016-08-122016-08-192016-08-262016-09-092016-09-162016-09-232016-09-302016-10-142016-10-212016-10-282016-11-112016-11-182016-11-252016-12-092016-12-162016-12-232016-12-302017-01-132017-01-202017-01-272017-02-102017-02-172017-02-242017-03-102017-03-172017-03-242017-03-312017-04-142017-04-212017-04-282017-05-122017-05-192017-05-262017-06-092017-06-162017-06-232017-06-302017-07-142017-07-212017-07-282017-08-112017-08-182017-08-252017-09-152017-09-222017-09-292017-10-132017-10-202017-10-272017-11-102017-11-172017-11-242017-12-152017-12-222017-12-292018-01-122018-01-192018-01-262018-02-092018-02-162018-02-232018-03-092018-03-162018-03-232018-03-302018-04-132018-04-202018-04-272018-05-112018-05-182018-05-252018-06-152018-06-222018-06-292018-07-132018-07-202018-07-272018-08-102018-08-172018-08-242018-08-312018-09-142018-09-212018-09-282018-10-122018-10-192018-10-262018-11-092018-11-162018-11-232018-11-302018-12-142018-12-212018-12-28`

`friday day < 8 in Jan 2015` returns `2015-01-02`

