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

# Examples
The following examples are generated based on tests run, so many results will be relative to the day it was tested. Every expression on the left side is valid syntax.

[//]: <> (BEGIN EXAMPLES)
`(T-1d).dow` returns `Sunday`

`(n + 180d)-180d == n` returns `True`

`(n + 181d)-180d != n` returns `True`

`(t + 180d)-180d == t` returns `True`

`-1d.dow` returns `Sunday`

`08h30` returns `8:30:00`

`1 in unix` returns `1`

`n - 1234` returns `18897 days, 14:15:39.405852`

`10h30 + 14h` returns `1 day, 0:30:00`

`2021 feb 14 12:00:00` returns `2021-02-14 12:00:00`

`seconds until 2021 feb 14 12:00:00` returns `-19438573.623969`

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

`1957-12-26 - t` returns `-23286 days, 0:00:00`

`1957-12-26 22:22:22 - t` returns `-23286 days, 22:22:22`

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

`6y5M4d3h2m1s` returns `2348 days, 3:02:00.999950`

`7y6M5w4d3h2m1.1s` returns `2777 days, 3:02:01.099955`

`2h2m` returns `2:02:00`

`3h+3M` returns `91 days, 2:59:59.999971`

`3M` returns `90 days, 23:59:59.999956`

`T-1.5d` returns `2021-09-25 12:00:00`

`T-10d` returns `2021-09-17`

`T.day` returns `27`

`T.dow` returns `Monday`

`YD.day` returns `26`

`n` returns `2021-09-27 11:36:18.363850`

`next Sunday` returns `2021-10-03`

`seconds until 3000 Apr 10` returns `30879491021.494247`

`seconds since 3000 Apr 10` returns `-30879491021.42555`

`next Sunday == last sunday` returns `False`

`next Sunday != last sunday` returns `True`

`last Sunday == next sunday` returns `False`

`last Sunday != next sunday` returns `True`

`last sunday in 2021` returns `2021-12-26`

`first sunday in 2021` returns `2021-01-03`

`t - next Sunday` returns `-6 days, 0:00:00`

`wait .001s` returns ``

`weekday 0` returns `Wednesday`

`Jan 2014` returns `2014-01-01`

`first friday in April 2014` returns `2014-04-04`

`first sun in April 2021` returns `2021-04-04`

`yd-5h` returns `2021-09-25 19:00:00`

`1957-12-26 22:22:22 in unix` returns `-379118258`

`5m+5m` returns `0:10:00`

`1h in seconds` returns `3600.0`

`1 hour in seconds` returns `3600.0`

`2s2s` returns `0:00:04`

`1996 August 28 9 AM` returns `1996-08-28 09:00:00`

`seconds until tomorrow` returns `44619.97283`

`seconds until 11 pm` returns `41019.905626`

`next month` returns `2021-10-01`

`first friday in next month` returns `2021-10-01`

`first friday in april` returns `2021-04-02`

`2014 01` returns `2014-01-01`

<!-- ## Examples -->
<!--  -->
<!-- ### date -->
<!-- `dte 1752 Sep 1` - returns that date -->
<!--  -->
<!-- `dte 1752 September 1 12 AM` - returns that date time -->
<!--  -->
<!-- `dte today - 1957-12-26 in days` - returns 23273.0 at the time of writing -->
<!--  -->
<!-- ### time -->
<!-- `dte 12h:00 AM + 4h` - returns 16:00:00  -->
<!--  -->
<!-- `dte 6 pm` - returns 18:00:00  -->
<!--  -->
<!-- `dte 23h:23` - returns 23:23:00 -->
<!--  -->
<!-- `dte 23m:23` - returns 00:23:23 -->
<!--  -->
<!-- The output format for time is configurable via the 'clock' key. -->
<!--  -->
<!-- ### week days -->
<!-- `dte monday` - returns the closest weekday date -->
<!--  -->
<!-- `dte last tuesday` - returns last tuesday's date -->
<!--  -->
<!-- `dte next tue` - returns next tuesday's date -->
<!--  -->
<!-- `dte 1611193453.dow` - returns `wednesday` in UTC-03:00 -->
<!--  -->
<!-- ### the `in` keyword -->
<!--  -->
<!-- `dte 1d in hours` - returns the amount of hours in a day -->
<!--  -->
<!-- `dte 1 day in hours` - returns the same as above -->
<!--  -->
<!-- `dte 2 hours 2 minutes in days` - returns 0.08472222222222221  -->
<!--  -->
<!-- `dte 1959 May 26 in unix` - returns the unix timestamp for the point in time -->
<!--  -->
<!-- ### the `until` keyword -->
<!--  -->
<!-- `dte seconds until tomorrow` - returns the amount of seconds until tomorrow -->
<!--  -->
<!-- `dte seconds until 3000 Apr 10` - returns the amount of seconds until date -->
<!--  -->
<!-- ### extremities -->
<!--  -->
<!-- `dte last sunday in 2021` - returns 2021-12-26 -->
<!--  -->
<!-- `dte first sunday in 2021` - returns 2021-01-03 -->
<!--  -->
<!-- ### basedate -->
<!--  -->
<!-- `dte 2021 Mar` - returns the specified first day of that basedate -->
<!--  -->
<!-- `dte days until Mar 2021` - returns the amount of days until the first day of base date -->
<!--  -->
<!-- `dte last sunday in Jan 2021` - returns 2021-01-31 -->
<!--  -->
<!-- ### operators -->
<!--  -->
<!-- `dte '2020 Jan 27 + 1y  == 2021 Jan 26'` - returns `True` -->
<!--  -->
<!-- `dte '12h:00 AM != 12h:00 PM'` - returns True -->
<!--  -->
<!-- ### delta declaration and operations -->
<!-- `dte 1d` - declares a one day timedelta -->
<!--  -->
<!-- `dte 7y6M5w4d3h2m1s` - represents 2776 days, 3:02:00 -->
<!--  -->
<!-- `dte 1d2m+2m+3h` - results in 1 day, 3:04:00 -->
<!--  -->
<!-- `dte -100.5d` - accepts negative and/or floating point values -->
<!--  -->
<!-- ### and in case you need it -->
<!-- `dte help` - prints a detailed manual -->
<!--  -->
<!-- ### locali(z|s)ation -->
<!-- `dte 2020 Okt 10` - would be valid input if user's locale is German -->
<!--  -->
<!-- ## Configuration File -->
<!--  -->
<!-- `dte` tries to read a `config.json` file under config directory (`~/.config/dte/` on Linux). In it you can set the following options: -->
<!-- @ -148,6 +68,212 @@ The output format for time is configurable via the 'clock' key. -->
<!--   - [ ] months -->
<!--   - [ ] units given current datetime field or second hand of `in` keyword -->
<!-- - [ ] run tests across a variety of locales -->
<!-- - [x] unify documentation by using tests -->
<!-- - [x] continuous integration -->
<!-- - [x] parse month & abbrev -->
<!-- - [x] parse weekday & abbrev -->
