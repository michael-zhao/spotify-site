from datetime import datetime, timedelta
import sys
import math

def main():
    in1 = sys.argv[1]
    in2 = sys.argv[2]
    if in1 == "today":
        d1 = datetime.today()
        week_diff = date_difference(d1, datetime.strptime(in2, '%m/%d/%Y'))
    else:
        week_diff = date_difference(datetime.strptime(in1, '%m/%d/%Y'), datetime.strptime(in2, '%m/%d/%Y'))
    print(week_diff)

def date_difference(d1, d2):
    return math.floor(abs((d2-d1).days / 7))

main()
