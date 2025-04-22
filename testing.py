from datetime import datetime, timedelta, timezone

from babel.dates import format_datetime

time = datetime.now(tz=timezone.utc) - timedelta(hours=6)
formatted = f"{format_datetime(
    time, "EEE, d MMM y HH:mm:ss", tzinfo=timezone.utc, locale="en"
)} GMT"
print(formatted)
