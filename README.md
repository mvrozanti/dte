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

## Examples

### date
`dte 1752 Sep 1` - returns that date

`dte 1752 September 1 12 AM` - returns that date time

`dte today - 1957-12-26 in days` - returns 23273.0 at the time of writing

### time
`dte 12h:00 AM + 4h` - returns 16:00:00 

`dte 6 pm` - returns 18:00:00 

`dte 23h:23` - returns 23:23:00

`dte 23m:23` - returns 00:23:23

The output format for time is configurable via the 'clock' key.

### week days
`dte monday` - returns the closest weekday date

`dte last tuesday` - returns last tuesday's date

`dte next tue` - returns next tuesday's date

`dte 1611193453.dow` - returns `wednesday` in UTC-03:00

### the `in` keyword

`dte 1d in hours` - returns the amount of hours in a day

`dte 1 day in hours` - returns the same as above

`dte 2 hours 2 minutes in days` - returns 0.08472222222222221 

`dte 1959 May 26 in unix` - returns the unix timestamp for the point in time

### the `until` keyword

`dte seconds until tomorrow` - returns the amount of seconds until tomorrow

`dte seconds until 3000 Apr 10` - returns the amount of seconds until date

### extremities

`dte last sunday in 2021` - returns 2021-12-26

`dte first sunday in 2021` - returns 2021-01-03

### basedate

`dte 2021 Mar` - returns the specified first day of that basedate

`dte days until Mar 2021` - returns the amount of days until the first day of base date

`dte last sunday in Jan 2021` - returns 2021-01-31

### operators

`dte '2020 Jan 27 + 1y  == 2021 Jan 26'` - returns `True`

`dte '12h:00 AM != 12h:00 PM'` - returns True

### delta declaration and operations
`dte 1d` - declares a one day timedelta

`dte 7y6M5w4d3h2m1s` - represents 2776 days, 3:02:00

`dte 1d2m+2m+3h` - results in 1 day, 3:04:00

`dte -100.5d` - accepts negative and/or floating point values

### and in case you need it
`dte help` - prints a detailed manual

### locali(z|s)ation
`dte 2020 Okt 10` - would be valid input if user's locale is German

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
  - [ ] `first/last friday in April` - extremity
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
- [x] continuous integration
- [x] parse month & abbrev
- [x] parse weekday & abbrev
