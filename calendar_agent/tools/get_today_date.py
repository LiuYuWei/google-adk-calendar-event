import datetime

def get_today_date():
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.date.today().strftime("%Y-%m-%d")
