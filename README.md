# University of Leeds Timetable Middleman

By default, the University of Leeds timetable served is very ugly, and can be hard to understand
at a glance. This project allows the user to act as a 'middleman' between the UoL timetable URL
and your calendar application of choice. When your calendar application requests the ICS file
from your link, the program will fetch the current UoL ICS file and reformat the summary & 
description to your taste.

## Prerequisites
 - Python 3
 - [icalendar pip](https://pypi.org/project/icalendar/)

## How to Use
Open the file & add your ICS file as given by the UoL timetable under 'Connect to calendar app'
as the variable `ICS_FILE`. If needed, modify the `EVENT_SUMMARY_FORMAT` & `EVENT_DESCRIPTION_FORMAT`.
Then, run the file & leave it running in the background. By default, the ICS file is hosted
as `http://localhost:9002/uol.ics`.

## Limitations
Since this program hosts only on `localhost`, there is no way to use this program as a middleman
to a cloud-based calendar application, such as Google Calendar.
