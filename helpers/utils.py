import calendar
from datetime import datetime

def get_current_month():
    # Get the current date
    current_date = datetime.now()

    # Get the current month and year
    current_month = current_date.month

    # Calculate the previous month and year
    previous_month = current_month 

    if previous_month == 0:
        previous_month = 12

    return calendar.month_name[previous_month]