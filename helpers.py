from datetime import datetime, timedelta
from database import Database

db = Database()

def normalize_to_midnight(dt: datetime):
    """Return a datetime at 00:00 (midnight) for the same day."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def check_and_reset_season():
    season_number, start_date = db.get_season_info()
    now = datetime.now()

    if not season_number: 
        season_number = 1
        start_date = normalize_to_midnight(now)
        db.new_season(season_number)
    
    start_date = normalize_to_midnight(start_date)

    next_reset = start_date + timedelta(days=30)
    next_reset = normalize_to_midnight(next_reset)

    if now >= next_reset:
        season_number += 1
        db.reset_points()
        start_date = normalize_to_midnight(now)
        db.new_season(season_number)
        next_reset = start_date + timedelta(days=30)

    days_left = (next_reset - now).days
    return season_number, days_left
