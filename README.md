# Date Time Expression

`dte` -- date time processing language


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

### Unix Timestamps
`dte 1611193453.dow` - returns `wednesday`

## To do
- [x] floating-point time units
- [x] subtract delta from date
- [x] add delta week month year
- [x] help
- [x] closest weekday
- [x] python-like comparison
- [ ] python-like conditional
- [x] wait(x)
- [x] timestamp object
- [x] next/last(weekday)
- [x] in keyword
- [ ] format(timepoint, fmt)
- [ ] add option to use locale
- [ ] add tab-completion 
- [ ] parse month & abbrev
- [x] parse weekday & abbrev
