import re
from datetime import datetime


def extract_date(input_str):
    current_date = datetime.now()

    date_pattern = r"(\d{1,2})(?:[-/.,\s])?(\d{1,2})?(?:[-/.,\s])?(\d{2,4})?"
    match = re.findall(date_pattern, input_str)[0]
    if not match:
        return None
    day, month, year = match
    day = int(day)

    if month:
        month = int(month)
    else:
        month = current_date.month

    if year:
        year = int(year)
    else:
        year = current_date.year

    try:
        extracted_date = datetime(year, month, day).strftime("%d.%m.%Y")
        return extracted_date
    except ValueError:
        return day, month, year
