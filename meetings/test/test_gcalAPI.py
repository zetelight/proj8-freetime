"""
Nose tests for google calendar API.
ONLY FOR PERSONAL TESTING PURPOSE.
Note: This test only works for my own calendar which means it may not work for others

"""

from flask_main import *
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = CONFIG.GOOGLE_KEY_FILE  # You'll need this
credentials = valid_credentials()
if not credentials:
    app.logger.debug("Redirecting to authorization")
gcal_service = get_gcal_service(credentials)
app.logger.debug("Returned from get_gcal_service")
calendars = list_calendars(gcal_service)
events = list_events(gcal_service, "test4CIS322XC@gmail.com")  # My testing email account


### Again, test cases below are fully based on my own calendar, so if other users want to test, they may have to write difference test cases.

def test_number_calendar():
    assert len(calendars) == 3


def test_number_event():
    assert len(events) == 3


def test_event_filter():
    event_list = []
    for event in events:
        if event_filter(event["start"]["dateTime"],
                        event["end"]["dateTime"],
                        "2017-11-06T22:00:00-08:00",
                        "2017-11-16T00:00:00-08:00"):
            # In my case, all events should be passed by this filter
            event_list.append(event)
    assert len(event_list) == 3


def test_calendar_list():

    assert calendars[0]["id"] == "test4CIS322XC@gmail.com"
    assert calendars[0]["summary"] == "test4CIS322XC@gmail.com"
    assert calendars[0]["description"] == "(no description)"

    assert calendars[0]["id"] == "#contacts@group.v.calendar.google.com"
    assert calendars[0]["summary"] == "Contacts"
    assert calendars[0]["description"] == "(no description)"

    assert calendars[0]["id"] == "en.usa#holiday@group.v.calendar.google.com"
    assert calendars[0]["summary"] == "Holidays in United States"
    assert calendars[0]["description"] == "(no description)""

def test_event_list():
    # since the events is sorted already by start_time, so we can check their contents one by one
    assert events[0]["id"] == "64sm2ohp70q38b9o6cqjgb9k6oq38bb170qjabb2ckpj2chi6thm6cb564"
    assert events[0]["summary"] == "test1"
    assert events[0]["start"]["dateTime"] == "2017-11-10T05:00:00-08:00"
    assert events[0]["end"]["dateTime"] == "2017-11-10T18:00:00-08:00"
    assert events[0]["description"] == "test boom!"

    assert events[1]["id"] == "70q3ie326kqjib9gckrmab9kc8s3gb9oc5hm8b9i6cqj2c1kc8s38o9o64"
    assert events[1]["summary"] == "test2"
    assert events[1]["start"]["dateTime"] == "2017-11-10T11:30:00-08:00"
    assert events[1]["end"]["dateTime"] == "2017-11-11T20:00:00-08:00"
    assert events[1]["description"] == "test papa!"

    assert events[2]["id"] == "c4s3id1hchij0bb4c8qm2b9k6ti3ibb260p62b9lc8pjcp31c8oj0d3264"
    assert events[2]["summary"] == "test3"
    assert events[2]["start"]["dateTime"] == "2017-11-12T15:30:00-08:00"
    assert events[2]["end"]["dateTime"] == "2017-11-14T08:30:00-08:00"
    assert events[2]["description"] == "test haha!"
