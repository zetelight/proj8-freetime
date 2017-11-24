"""
Nose tests for event
"""
import sys
sys.path.append("..")
from Model import CalendarEvent

event1 = CalendarEvent("14:30:00-08:00", "21:30:00-08:00", "2014/01/01", status="BUSY")
event2 = CalendarEvent("07:30:00-08:00", "14:30:00-08:00", "2014/01/05", status="BUSY")
event3 = CalendarEvent("01:30:00-08:00", "11:30:00-08:00", "2014/01/05", status="BUSY")
event4 = CalendarEvent("14:22:00-08:00", "17:12:00-08:00", "2014/01/05", status="BUSY")
event5 = CalendarEvent("04:11:00-08:00", "18:24:00-08:00", "2014/01/05", status="BUSY")


def test_event_compare():
    assert (event1 > event2) == False
    assert (event2 < event3) == False
    assert (event3 < event4) == True


def test_overlap():
    assert event2.overlap(event3) == True
    assert event4.overlap(event5) == True
    assert event3.overlap(event1) == False


def test_union():
    event6 = event2.union(event3)
    assert event6.get_start() == "01:30:00-08:00"
    assert event6.get_end() == "14:30:00-08:00"
    assert event6.get_date() == "2014/01/05"
    event7 = event4.union(event5)
    assert event7.get_start() == "04:11:00-08:00"
    assert event7.get_end() == "18:24:00-08:00"
    assert event7.get_date() == "2014/01/05"

