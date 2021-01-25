# Date Time Expression

![PyPI](https://img.shields.io/pypi/v/dte)
![Travis (.com)](https://img.shields.io/travis/com/mvrozanti/dte)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dte)

`dte` is a WIP date-time processing language with focus on broad interpretation and simplicity.

If you don't think it's intuitive, it's probably not finished.

It is strongly inspired by [pdd](https://github.com/jarun/pdd).

## How to use & What to know

### Install

`pip install dte`


- Dates are always interpreted with highest units appearing before, e.g.: `%Y-%m-%d` or `%Y %b %d` formats, although the unit separator doesn't have to be "-" for the former
- Unix timestamps are both interpreted and output in seconds
- `help` is a command

### Dependencies
- [dateutil](https://github.com/dateutil/dateutil), which handle month and year's complex operations
- [ply](https://github.com/dabeaz/ply), which is a python implementation of lex and yacc

## Examples

### date difference
`dte 1957-12-26 - today`

### week days
`dte monday` - returns the closest weekday date

`dte last tuesday` - returns last tuesday's date

`dte next tue` - returns next tuesday's date

`dte 1611193453.dow` - returns `wednesday` in UTC-03:00

### the `in` keyword

`dte 1d in hours` - returns the amount of hours in a day

`dte 1959 Jan 26 in unix` - returns the unix timestamp for the date

### operators

`dte '2019 June 27 + 9y > 2000 Jan 01'` - returns `True`

### delta declaration and operations
`dte 1d` - declares a one day timedelta

`dte 7y6m5w4d3h2M1s` - represents 2776 days, 3:02:00

`dte 1d2M+2M+3h` - results in 1 day, 3:04:00

`dte -100.5d` - accepts negative and/or floating point values

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
- [x] in keyword
  - [ ] add geolocation? `18H:00 in England`?
  - [ ] `last friday in 2014`
  - [ ] `last friday in April`
  - [ ] `last friday in April 2014`
- [ ] format(timepoint, fmt) (in keyword)units given current time field
- [ ] add option to use locale or custom formats for i/o
- [ ] add tab-completion for:
  - [ ] months
  - [ ] units given current time field or second hand of `in` keyword
- [ ] continuous integration
- [x] parse month & abbrev
- [x] parse weekday & abbrev
