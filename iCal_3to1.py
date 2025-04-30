import requests
from ics import Calendar, Event
from datetime import datetime, time, timedelta, timezone
import pytz

# Use your local timezone
local_tz = pytz.timezone("Europe/Copenhagen")


# Calendar URLs and their labels
calendar_sources = {
    "https://landfolk.com/l/620bc23f/calendar.ics?t=TzV2uz9oxrTZuwTVNnbWebU3": "Landfolk",
    "https://www.campaya.dk/calendar/ical/147226.ics?s=a6959ef6208c4db09b6a9fab9c2f9eae": "Campaya",
    "https://www.airbnb.dk/calendar/ical/7444875.ics?s=684d2119066004d0ea92541480d27e00": "Airbnb"
}


##calendar_sources = {"https://www.airbnb.dk/calendar/ical/7444875.ics?s=684d2119066004d0ea92541480d27e00": "Airbnb"
##}


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


##calendar = Calendar()
##
##for start, end, source in booked_periods:
##    e = Event()
##    e.name = f"Booked ({source})"
##    e.begin = start
##    e.end = end
##    e.make_all_day()
##    calendar.events.add(e)
##
### Save the calendar to a file (or return it as string for hosting)
##with open("bookings.ics", "w") as f:
##    f.writelines(calendar)
##
##
### Save the calendar to C:\temp\bookings.ics
##output_path = r"C:\temp\bookings.ics"
##with open(output_path, "w", encoding="utf-8") as f:
##    f.writelines(calendar)
##
##print(f".ics file saved to: {output_path}")



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
output_path = r"C:\temp\DownTownSkagen_SourceAndTime.ics"
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(calendar2)

print(f".ics file with timed bookings saved to: {output_path}")
