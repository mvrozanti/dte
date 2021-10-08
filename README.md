# Date Time Expression

![PyPI](https://img.shields.io/pypi/v/dte)
![Travis (.com)](https://img.shields.io/travis/com/mvrozanti/dte)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dte)

`dte` is a WIP date-time processing language with focus on broad interpretation and simplicity.

If you don't think it's intuitive, it's most likely unfinished.

It is strongly inspired by [pdd](https://github.com/jarun/pdd).

## How to use & What to know

`pip install dte`

### Conventions
![relevant xkcd](https://sslimgs.xkcd.com/comics/iso_8601.png)
- When there is margin for ambiguity, expressions are always interpreted with [highest units appearing before](https://i.imgur.com/y2tBVHx.png), e.g.: `2021-06-13`, `2023 August 27` or `2019 Jul 20`
- Unix timestamps are both interpreted and output in seconds by default, but this is configurable
- When specifying time, just remember that `M` is for month and `m` is for minute
- Although english month and week-day names are always recognized, so are the names in the user's locale

## Configuration File

`dte` tries to read a `config.json` file under config directory (`~/.config/dte/` on Linux). In it you can set the following options:

```
{
  "timestamp_unit": "<seconds|milliseconds>"
  "clock": "<24|12>",
  "datetime_output_format": "<ISO8601|<format>>"
  "comparison_tolerance_seconds": <seconds>
  "comparison_tolerance_seconds": <seconds>
  "basedate_output_format": "%Y-%b",
}
```

### Dependencies
- [dateutil](https://github.com/dateutil/dateutil) handles month and year's complex operations
- [ply](https://github.com/dabeaz/ply) is a pure-Python implementation of the popular compiler construction tools lex and yacc 
- [appdirs](https://github.com/ActiveState/appdirs) for reading config file in a cross-platform manner

## To do
- [x] floating-point time units
- [x] subtract delta from date
- [x] add delta week month year
- [x] help
- [x] closest weekday
- [x] python-like comparison
- [x] wait(x)
- [x] timestamp object
- [x] next/last(weekday)
- [x] add basedate point
- [x] add `6 pm`
- [x] in keyword
  - [x] `first/last friday in 2014` - extremity
  - [x] `first/last friday in April` - extremity
  - [x] `first/last friday in next month` - extremity
  - [x] `first/last friday in 2014 April ` - extremity
  - [ ] `INTEGERth WEEKDAY IN BASEDATE` - extremity?
- [x] until keyword
- [ ] format(timepoint, fmt) (in keyword) units given current time field
- [ ] add option
  - [ ] to use custom locale
  - [x] to set unix timestamp format (seconds, millis, etc)
- [ ] add tab-completion for:
  - [ ] months
  - [ ] units given current datetime field or second hand of `in` keyword
- [ ] run tests across a variety of locales
- [x] unify documentation by using tests
- [x] continuous integration
- [x] parse month & abbrev
- [x] parse weekday & abbrev
- [ ] add `show` function
  - [ ] show clock for time
  - [ ] show cal for date and basedate

# Examples
The following examples are generated based on tests run, so many results will be relative to the day it was tested. Every expression on the left side is valid syntax.

[//]: <> (BEGIN EXAMPLES)
`(T-1d).dow` returns `Thursday`

`(n + 180d)-180d == n` returns `True`

`(n + 181d)-180d != n` returns `True`

`(t + 180d)-180d == t` returns `True`

`-1d.dow` returns `Thursday`

`08h30` returns `8:30:00`

`1 in unix` returns `1`

`n - 1234` returns `18908 days, 14:02:23.144316`

`10h30 + 14h` returns `1 day, 0:30:00`

`2021 feb 14 12:00:00` returns `2021-02-14 12:00:00`

`seconds until 2021 feb 14 12:00:00` returns `-20388177.361474`

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

`1610494238+4h.dow` returns `Wednesday`

`1610494238.dow` returns `Tuesday`

`12h:00 AM != 12h:00 PM` returns `True`

`2014 Jan 13==2014 January 13` returns `True`

`1957-12-26 - t` returns `-23297 days, 0:00:00`

`1957-12-26 22:22:22 - t` returns `-23297 days, 22:22:22`

`1958-05-14 - 1958-05-16` returns `-2 days, 0:00:00`

`1d in hours` returns `24.0`

`1d in minutes` returns `1440.0`

`1d in seconds` returns `86400.0`

`1d` returns `1 day, 0:00:00`

`1d+0h22m` returns `1 day, 0:22:00`

`1d1m in hours` returns `24.016666666666666`

`1970 Jan 1 - 3h in unix` returns `0`

`1w` returns `7 days, 0:00:00`

`2020 Jan 27 + 1y == 2021 Jan 26` returns `True`

`2 < 1` returns `False`

`12h:00 pm != 12h:00 am` returns `True`

`22h+2m` returns `22:02:00`

`22h22m` returns `22:22:00`

`6y5M4d3h2m1s` returns `2346 days, 3:02:00.999955`

`7y6M5w4d3h2m1.1s` returns `2778 days, 3:02:01.099954`

`2h2m` returns `2:02:00`

`3h+3M` returns `92 days, 2:59:59.999971`

`3M` returns `91 days, 23:59:59.999970`

`T-1.5d` returns `2021-10-06 12:00:00`

`T-10d` returns `2021-09-28`

`T.day` returns `8`

`T.dow` returns `Friday`

`YD.day` returns `7`

`n` returns `2021-10-08 11:23:01.914624`

`next Sunday` returns `2021-10-10`

`seconds until 3000 Apr 10` returns `30878541417.93545`

`seconds since 3000 Apr 10` returns `-30878541417.862812`

`next Sunday == last sunday` returns `False`

`next Sunday != last sunday` returns `True`

`last Sunday == next sunday` returns `False`

`last Sunday != next sunday` returns `True`

`last sunday in 2021` returns `2021-12-26`

`first sunday in 2021` returns `2021-01-03`

`t - next Sunday` returns `-2 days, 0:00:00`

`wait .001s` returns ``

`weekday 0` returns `Wednesday`

`Jan 2014` returns `2014-01-01`

`first friday in April 2014` returns `2014-04-04`

`first sun in April 2021` returns `2021-04-04`

`yd-5h` returns `2021-10-06 19:00:00`

`1957-12-26 22:22:22 in unix` returns `-379118258`

`5m+5m` returns `0:10:00`

`1h in seconds` returns `3600.0`

`1 hour in seconds` returns `3600.0`

`2s2s` returns `0:00:04`

`1996 August 28 9 AM` returns `1996-08-28 09:00:00`

`seconds until tomorrow` returns `45416.403841`

`seconds until 11 pm` returns `41816.326001`

`next month` returns `2021-11-01`

`first friday in next month` returns `2021-11-05`

`first friday in april` returns `2021-04-02`

`2014 01` returns `2014-01-01`

`6pm+1h` returns `19:00:00`

`days until 2030-12-25` returns `3364.525646829919`

`last fri in 2014 December` returns `2014-12-26`

`last fri in 2014 Dec` returns `2014-12-26`

`last fri in Dec 2014` returns `2014-12-26`

`yesterday==thursday` returns `True`

`yesterday==thu` returns `True`

