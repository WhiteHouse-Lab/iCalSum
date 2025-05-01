import requests
from ics import Calendar, Event
from datetime import datetime, time, timedelta, timezone
import pytz
import os

# Use your local timezone
local_tz = pytz.timezone("Europe/Copenhagen")


# Calendar URLs and their labels
calendar_sources = {
    "https://landfolk.com/l/620bc23f/calendar.ics?t=TzV2uz9oxrTZuwTVNnbWebU3": "Landfolk, Penthouse",
    "https://www.campaya.dk/calendar/ical/147226.ics?s=a6959ef6208c4db09b6a9fab9c2f9eae": "Campaya, Penthouse",
    "https://www.airbnb.dk/calendar/ical/7444875.ics?s=684d2119066004d0ea92541480d27e00": "Airbnb, Penthouse",
    "https://ical.booking.com/v1/export?t=94fb4af9-132f-4307-a7b8-f07eb8691130": "Booking, Lejl. 5",
    "https://www.airbnb.dk/calendar/ical/1391100679122939389.ics?s=f2377d8e9bbde9df063061bf069f32c5": "Airbnb, Lejl. 5"
}

# Define the time limit: 2 months ago
cutoff_date = datetime.now(timezone.utc) - timedelta(days=60)

# Function to fetch and parse events
def fetch_events(url, label):
    response = requests.get(url)
    response.raise_for_status()
    calendar = Calendar(response.text)
    return [(event.begin.date(), event.end.date(), label) for event in calendar.events if event.end and event.end > cutoff_date]

# Collect booked periods
booked_periods = []

for url, label in calendar_sources.items():
    try:
        events = fetch_events(url, label)
        booked_periods.extend(events)
    except Exception as e:
        print(f"Error fetching from {url}: {e}")

# --- Output 1: Simple List ---
print("\n=== Booked Periods (Simple List) ===")
for start, end, _ in sorted(booked_periods):
    print(f"Booked: {start} to {end}")

# --- Output 2: With Source Info ---
print("\n=== Booked Periods (With Source) ===")
for start, end, source in sorted(booked_periods):
    print(f"{source}: {start} to {end}")



#Standard full Day Bookings


calendar = Calendar()

for start, end, source in booked_periods:
    e = Event()
    e.name = f"Optaget ({source})"
    e.begin = start
    e.end = end
    e.make_all_day()
    calendar.events.add(e)

# Save to root
output_path = os.path.join(os.getcwd(), "DownTownSkagen_All_Sources.ics")
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(calendar)



# 1600 - 1000 bookings
calendar2 = Calendar()

for start_date, end_date, source in booked_periods:
    # Create aware datetime objects with correct time and timezone
    start_naive = datetime.combine(start_date, time(16, 0))
    end_naive = datetime.combine(end_date, time(10, 0))
    start = local_tz.localize(start_naive)
    end = local_tz.localize(end_naive)

    event = Event()
    event.name = f"Booked ({source})"
    event.begin = start
    event.end = end
    calendar2.events.add(event)

# Save to C:\temp\
output_path = os.path.join(os.getcwd(), "DownTownSkagen_SourceAndTime.ics")
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(calendar2)

print(f".ics file with timed bookings saved to: {output_path}")
