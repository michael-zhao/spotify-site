"""
Module with a method that calculates the difference (in weeks, for now) between two dates.
"""
from datetime import datetime
import sys
import math

def main():
    """Main method."""
    in1 = sys.argv[1]
    in2 = sys.argv[2]
    if in1 == "today":
        d1 = datetime.today()
        week_diff = date_difference(d1, datetime.strptime(in2, '%Y/%m/%d'))
    else:
        week_diff = date_difference(
            datetime.strptime(in1, '%Y/%m/%d'), datetime.strptime(in2, '%Y/%m/%d'))
    print(week_diff)

def date_difference(d1, d2):
    """Returns the date difference."""
    return math.floor(abs((d2-d1).days / 7))

main()
