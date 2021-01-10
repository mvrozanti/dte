#!/bin/bash
{
    echo 'T'     | ./dtc || exit 1
    echo 'T-10D' | ./dtc || exit 3
} 2>&1 >/dev/null
exit 0
# echo 'T-D'   | ./dtc || exit 4
# echo 'Ta'    | ./dtc && exit 2
