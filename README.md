# Date Time Expression
## To do
- [x] floating-point time units
- [ ] parse month & abbrev
- [ ] parse weekday & abbrev
- [x] add delta week month year
- [x] closest weekday
- [x] python-like comparison
- [ ] python-like conditional
- [x] next/last(weekday)
- [x] timestamp object
- [x] wait(x)
- [ ] format(timepoint)
- [ ] tu(delta) / in keyword
- [x] subtract delta from date
- [x] help


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


