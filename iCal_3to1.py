import requests
from ics import Calendar, Event
from datetime import datetime, timedelta, timezone
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

# Function to fetch and parse events (updated to include summary)
def fetch_events(url, label):
    response = requests.get(url)
    response.raise_for_status()
    calendar = Calendar(response.text)
    return [
        {
            "start": event.begin.date(),
            "end": event.end.date(),
            "label": label,
            "summary": event.name if event.name else "No Summary"
        }
        for event in calendar.events if event.end and event.end > cutoff_date
    ]

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
for event in sorted(booked_periods_L5, key=lambda x: x["start"]):
    print(f"Booked: {event['start']} to {event['end']}")

# --- Output 2: With Source Info booked_periods_PH ---
print("\n=== booked_periods_PH (With Source) ===")
for event in sorted(booked_periods_PH, key=lambda x: x["start"]):
    print(f"{event['label']}: {event['start']} to {event['end']} (Summary: {event['summary']})")

# Standard full Day Bookings Penthouse
Booked_PH = Calendar()

for event in booked_periods_PH:
    e = Event()
    # Use "Privat Booking" if summary contains "Airbnb (Not available)"
    if "Airbnb (Not available)" in event['summary']:
        e.name = "Privat, Penthouse"
    else:
        e.name = f"Optaget ({event['label']})"
    e.begin = event['start']
    e.end = event['end'] - timedelta(days=1)  # Subtract one day from end date
    e.make_all_day()  # Ensure it's a full-day event
    Booked_PH.events.add(e)

# Save to root
output_path = os.path.join(os.getcwd(), "Booked_PH.ics")
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(Booked_PH)

# Standard full Day L5
Booked_L5 = Calendar()

for event in booked_periods_L5:
    e = Event()
    # Use "Privat Booking" if summary contains "Airbnb (Not available)"
    if "Airbnb (Not available)" in event['summary']:
        e.name = "Privat, Lejl 5"
    else:
        e.name = f"Optaget ({event['label']})"
    e.begin = event['start']
    e.end = event['end'] - timedelta(days=1)  # Subtract one day from end date
    e.make_all_day()  # Ensure it's a full-day event
    Booked_L5.events.add(e)

# Save to root
output_path = os.path.join(os.getcwd(), "Booked_L5.ics")
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(Booked_L5)

print(f".ics file with Bookings saved to: {output_path}")


# --- Additional Public_PH.ics ---
Public_PH = Calendar()

for event in booked_periods_PH:
    e = Event()
    e.name = "Penthouse Optaget"  # Set the name for public visibility
    e.begin = event['start']
    e.end = event['end'] - timedelta(days=1)  # Subtract one day from end date
    e.make_all_day()  # Ensure it's a full-day event
    Public_PH.events.add(e)

# Save Public_PH.ics to root
public_ph_path = os.path.join(os.getcwd(), "Public_PH.ics")
with open(public_ph_path, "w", encoding="utf-8") as f:
    f.writelines(Public_PH)

# --- Additional Public_L5.ics ---
Public_L5 = Calendar()

for event in booked_periods_L5:
    e = Event()
    e.name = "Pakhus Optaget"  # Set the name for public visibility
    e.begin = event['start']
    e.end = event['end'] - timedelta(days=1)  # Subtract one day from end date
    e.make_all_day()  # Ensure it's a full-day event
    Public_L5.events.add(e)

# Save Public_L5.ics to root
public_l5_path = os.path.join(os.getcwd(), "Public_L5.ics")
with open(public_l5_path, "w", encoding="utf-8") as f:
    f.writelines(Public_L5)

print(f"Public .ics files saved to: {public_ph_path} and {public_l5_path}")
