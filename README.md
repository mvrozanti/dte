# Date Time Expression

![PyPI](https://img.shields.io/pypi/v/dte)

# How to use
For general use just keep in mind:

- Dates are always interpreted with highest units appearing before, e.g.: `%Y-%m-%d` or `%Y %b %d` formats, although the unit separator doesn't have to be - for the former
- Unix timestamps are both interpreted and output in seconds
- Month and year's complex operations are handled by [dateutil](https://github.com/dateutil/dateutil) module
- `help` is a command

## Examples

### date difference
`dte 1957-12-26 - today`

### week days
`dte 'next sunday; last monday'` 
- takes a week day as argument and returns

`dte monday` - returns the closest weekday date

`dte last tuesday` - returns last tuesday's date

`dte next tue` - returns next tuesday's date

`dte 1611193453.dow` - returns `wednesday`

### unit conversion

`dte 1d in hours`

### delta declaration and operations
`dte 6y5m4d3h2M1s`
`dte 1d2M+2M+3h`
`dte -100.5d`

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
  - [ ] last friday in `2014`
  - [ ] last friday in `April`
  - [ ] last friday in `April 2014`
- [ ] format(timepoint, fmt) (in keyword)units given current time field
- [ ] add option to use locale or custom formats for i/o
- [ ] add tab-completion for:
  - [ ] Months
  - [ ] units given current time field or second hand of `in` keyword
- [ ] continuous integration
- [x] parse month & abbrev
- [x] parse weekday & abbrev
