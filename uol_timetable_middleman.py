"""
UoL Timetable Middleman

A script for formatting the default ICS provided by the University of Leeds
timetable into one which can be more easily understood, then hosting it as
a URL a calendar application can request.

By Jacqueline W., 2025
Based on an idea by Harry B.
"""

import urllib.request
import icalendar
import re

from http.server import BaseHTTPRequestHandler, HTTPServer

"""
Recognized tokens for formatting:
    %draft% - if event is draft, '[Draft]', else ''
    %code% - module code is placed
    %name% - module name
    %type% - session type
    %loc% - campus location
    %staff% - staff members
"""

ICS_LINK = ""

EVENT_SUMMARY_FORMAT = "%draft%%type% - %name%"
EVENT_DESCRIPTION_FORMAT = "%code% - %name%\nLocation: %loc%\nStaff: %staff%"

PORT = 9002

class ICSRequestHandler(BaseHTTPRequestHandler):
    """Handles request for ICS file"""

    """Gets ICS file from link and created Calendar obj from file"""
    def get_ics_from_link(self, link):
        ics_f = urllib.request.urlopen(link)
        ics = icalendar.Calendar.from_ical(ics_f.read())

        return ics
    
    """Generates dict of tokens from given event. Token keys are as above."""
    def generate_toks_from_event(self, event):
        tok_dict = {}

        #%draft%
        summary = event.get("SUMMARY")
        if re.search("([DRAFT])", summary) is None:
            tok_dict["%draft%"] = ""
        else:
            tok_dict["%draft%"] = "[Draft] "

        description = event.get("DESCRIPTION")
    
        #%code%
        code_match = re.search("Module code: (.*)", description)
        if code_match is None:
            tok_dict["%code%"] = ""
        else:
            tok_dict["%code%"] = code_match.group(1)

        #%name%
        name_match = re.search("Module Name: (.*)", description)
        if name_match is None:
            tok_dict["%name%"] = ""
        else:
            tok_dict["%name%"] = name_match.group(1)

        #%type%
        type_match = re.search("Activity/Session Type: (.*)", description)
        if type_match is None:
            tok_dict["%type%"] = ""
        else:
            tok_dict["%type%"] = type_match.group(1)

        #%loc%
        location = event.get("LOCATION")
        tok_dict["%loc%"] = str(location)

        #%staff%
        staff_match = re.search("Staff member\(s\): (.*)", description)
        if staff_match is None:
            tok_dict["%staff%"] = ""
        else:
            tok_dict["%staff%"] = staff_match.group(1)

        return tok_dict

    """Generates reformatted ICS file from provided ICS_LINK,
       returns bytestring"""
    def generate_content(self):
        ics = self.get_ics_from_link(ICS_LINK)

        for event in ics.events:
            tok_dict = self.generate_toks_from_event(event)

            summary_line = EVENT_SUMMARY_FORMAT
            description_line = EVENT_DESCRIPTION_FORMAT

            for key, value in tok_dict.items():
                summary_line = summary_line.replace(key, value)
                description_line = description_line.replace(key, value)

            event["SUMMARY"] = summary_line
            event["DESCRIPTION"] = description_line

        return ics.to_ical()

    """Handles all GET reqs for server. Only responds to GET /uol.ics"""
    def do_GET(self):
        if self.path == "/uol.ics":
            self.send_response(200)
            self.send_header("Content-type", "text/calendar")
            self.end_headers()

            formatted_ics = self.generate_content()
            self.wfile.write(formatted_ics)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

server_address = ("", PORT)
httpd = HTTPServer(server_address, ICSRequestHandler)
httpd.serve_forever()
