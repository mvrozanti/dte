# Date Time Expression

![PyPI](https://img.shields.io/pypi/v/dte)

# How to use
For general use just keep in mind:

- Dates are always interpreted with highest units appearing before, e.g.: `%Y-%m-%d` or `%Y %b %d` formats, although the unit separator doesn't have to be - for the former
- Unix timestamps are both interpreted and output in seconds
- Month and year's complex operations are handled by [dateutil](https://github.com/dateutil/dateutil) module

## Examples

### date difference
`dte 1957-12-26 - today`

### `wait`

`dte wait .1s` 
- waits for a tenth of a second and exits

### `last` and `next`
`dte 'next sunday; last monday'` 
- takes a week day as argument and returns

### `WEEKDAY`
`dte monday` - returns the closest weekday date

`dte last tuesday` - returns last tuesday's date

`dte next tuesday` - returns next tuesday's date

### Unix Timestamps
`dte 1611193453.dow` - returns `wednesday`

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
  - [ ] last friday in <month>
- [ ] format(timepoint, fmt)
- [ ] add option to use locale for output format
- [ ] add tab-completion 
- [x] parse month & abbrev
- [x] parse weekday & abbrev
