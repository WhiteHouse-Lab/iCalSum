import requests
from ics import Calendar, Event
from datetime import datetime, time, timedelta, timezone
import pytz
import os

# Use your local timezone
local_tz = pytz.timezone("Europe/Copenhagen")


# Penthouse - Calendar URLs and their labels (PH)
ical_sources_PH = {
    "https://landfolk.com/l/620bc23f/calendar.ics?t=TzV2uz9oxrTZuwTVNnbWebU3": "Landfolk, Penthouse",
    "https://www.campaya.dk/calendar/ical/147226.ics?s=a6959ef6208c4db09b6a9fab9c2f9eae": "Campaya, Penthouse",
    "https://www.airbnb.dk/calendar/ical/7444875.ics?s=684d2119066004d0ea92541480d27e00": "Airbnb, Penthouse",
}

# Lejlighed 5 - Calendar URLs and their labels (L5)
ical_sources_L5 = {
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


# Get dicts using Function above
booked_periods_PH = []
for url, label in ical_sources_PH.items():
    try:
        events = fetch_events(url, label)
        booked_periods_PH.extend(events)
    except Exception as e:
        print(f"Error fetching from {url}: {e}")

# Get dicts using Function above
booked_periods_L5 = []
for url, label in ical_sources_L5.items():
    try:
        events = fetch_events(url, label)
        booked_periods_L5.extend(events)
    except Exception as e:
        print(f"Error fetching from {url}: {e}")


# --- Output 1: Simple List booked_periods_L5 ---
print("\n=== booked_periods_L5 (Simple List) ===")
for start, end, _ in sorted(booked_periods_L5):
    print(f"Booked: {start} to {end}")

# --- Output 2: With Source Info booked_periods_PH ---
print("\n=== booked_periods_PH (With Source) ===")
for start, end, source in sorted(booked_periods_PH):
    print(f"{source}: {start} to {end}")


#--------------------------------------

#Standard full Day Bookings Penthouse

Booked_PH = Calendar()

for start, end, source in booked_periods_PH:
    e = Event()
    e.name = f"Optaget ({source})"
    e.begin = start
    e.end = end
    e.make_all_day()
    Booked_PH.events.add(e)

# Save to root
output_path = os.path.join(os.getcwd(), "Booked_PH.ics")
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(Booked_PH)


#Standard full Day L5

Booked_L5 = Calendar()

for start, end, source in booked_periods_L5:
    e = Event()
    e.name = f"Optaget ({source})"
    e.begin = start
    e.end = end
    e.make_all_day()
    Booked_L5.events.add(e)

# Save to root
output_path = os.path.join(os.getcwd(), "Booked_L5.ics")
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(Booked_L5)
    
print(f".ics file with Bookings saved to: {output_path}")

#---------------------------------------------


