"""
A class for time chunk on google calendar
Credits: agenda.py from Professor Young
"""
import datetime

BUSY = "BUSY"
FREE = "FREE"


class CalendarEvent(object):
    def __init__(self, start_time, end_time, date, summary = None, description = None, id = None, status=BUSY):
        """
        Initialization method for CalendarEvent
        Args:
            start_time: a time without date, start time of one event
            end_time: a time without date, end time of one event
                Example for time: "14:30:00-08:00"
            date: a date of a even
                Example for date: "2014/01/01"
            summary: a list, the summary of the event
            status: a string, shows 'busy' or 'free'
            description: a string, the content of the event
        Note: I use s_time and e_time to represent the time in one day. 
              If the start/end time is like above, the s/e time will be 14:30:00-08:00
              I use it to compute one day's event
        """
        self.start = start_time
        self.end = end_time
        self.date = date
        self.summary = summary
        self.description = description
        self.id = id
        self.status = status

    def __repr__(self):
        return "start:" + self.start + \
                "end: " + self.end + \
                "date: " + self.date + \
                "status: " + self.status + \
                "summary: " + self.summary + \
                "description: " + self.description

    def get_start_time(self):
        """
        get the start time to sort
        """
        return self.assemble_time(self.start)

    def get_end_time(self):
        """
        get the end time to sort
        """
        return self.assemble_time(self.end)

    def get_date(self):
        """
        get the end time to sort
        """
        return self.date
    
    def get_id(self):
        """
        get the id
        """
        return self.id

    def assemble_time(self, time):
        """
        translate time to be ISO formate
        """
        iso_time = self.date + "T" + time
        return iso_time
    
    def __lt__(self, other):
        """
        compare time.
        Return:
            True if and only if the other is done by the time this event begins
        """
        return self.end <= other.start

    def __gt__(self, other):
        """
        compare time.
        Return:
            True if and only if the other is done before the time this event begins
        """
        return other < self

    def overlap(self, other):
        """
        check whether events are overlap
        """
        return not (self < other or other < self)

    def translator(self):
        """
        translate event class object to a list of dictionaries
        Args:
            self: a CalendarEvent object
        return;
            dictionary: a dictionaries, which is a event
        """
        event = {}
        event["id"] = self.id
        event["start_time"] = self.assemble_time(self.start)
        event["end_time"] = self.assemble_time(self.end)
        event["summary"] = self.summary
        event["description"] = self.description
        event["status"] = self.status
        return event

    def time_union(self, other):
        """
        get the time union of two event if they are overlapped
        Args:
            other: another event object
        Return:
            return a new unioned event
        """
        new_start = min(self.start, other.start)
        new_end = max(self.end, other.end)
        return CalendarEvent(new_start, new_end, self.date)

    def time_list(self, other):
        """
        get the time list of two event if they are not overlapped
        Args:
            other: another event object
        Return:
            return a new time list which 
        """
        time_list = []
        time_list.append(self)
        time_list.append(other)
        return time_list

    def free_time(self, busy_time):
        """
        The crucial method is for computing free time. Use a whole day object
        to  substract busy time object.
        I hardcode here because I don't have time to give an elegant solution
        Args:
            busy_time: a event object, indicating busy block
        Return:
            free_list: a list of free time, indicating free blocks
        """
        free_list = []
        if (busy_time.start >= self.start and busy_time.end < self.end):
            free_list.append(CalendarEvent(busy_time.end, self.end, self.date))
        elif (busy_time.end >= self.end and busy_time.start < self.start):
             free_list.append(CalendarEvent(busy_time.end, self.end, self.date))
        elif (busy_time.start >= self.start and busy_time.end >= self.end:
            pass                                                                                                






# Class Agenda is from agenda.py whose author is Professor Young
# I tried to make my own agenda but it really takes time
# so I decieded to use professor's one but revised some codes to complete my project

class Agenda(object):
    """An Agenda is essentially a list of appointments,
    with some agenda-specific methods.
    """

    def __init__(self):
        """An empty agenda."""
        self.appts = [ ]

    def append(self,appt):
        """Add an Appt to the agenda."""
        self.appts.append(appt)

    def intersect(self,other,desc=""): 
        """Return a new agenda containing appointments
        that are overlaps between appointments in this agenda
        and appointments in the other agenda.

        Titles of appointments in the resulting agenda are
        taken from this agenda, unless they are overridden with
        the "desc" argument.

        Arguments:
           other: Another Agenda, to be intersected with this one
           desc:  If provided, this string becomes the title of
                all the appointments in the result.
        """
        default_desc = (desc == "")
        result = Agenda()
        for thisappt in self.appts:
            if default_desc: 
                desc = thisappt.desc
            for otherappt in other.appts:
                if thisappt.overlaps(otherappt):
                    result.append(thisappt.intersect(otherappt,desc))
        
        return result

    def normalize(self):
        """Merge overlapping events in an agenda. For example, if 
        the first appointment is from 1pm to 3pm, and the second is
        from 2pm to 4pm, these two are merged into an appt from 
        1pm to 4pm, with a combination description.  
        After normalize, the agenda is in order by date and time, 
        with no overlapping appointments.
        """
        if len(self.appts) == 0:
            return

        ordering = lambda ap: ap.begin
        self.appts.sort(key=ordering)

        normalized = [ ]
        # print("Starting normalization")
        cur = self.appts[0]  
        for appt in self.appts[1:]:
            if appt > cur:
                # Not overlapping
                # print("Gap - emitting ", cur)
                normalized.append(cur)
                cur = appt
            else:
                # Overlapping
                # print("Merging ", cur, "\n"+
                #      "with    ", appt)
                cur = cur.union(appt)
                # print("New cur: ", cur)
        # print("Last appt: ", cur)
        normalized.append(cur)
        self.appts = normalized

    def normalized(self):
        """
        A non-destructive normalize
        (like "sorted(l)" vs "l.sort()").
        Returns a normalized copy of this agenda.
        """
        copy = Agenda()
        copy.appts = self.appts
        copy.normalize()
        return copy
        
    def complement(self, freeblock):
        """Produce the complement of an agenda
        within the span of a timeblock represented by 
        an appointment.  For example, 
        if this agenda is a set of appointments, produce a 
        new agenda of the times *not* in appointments in 
        a given time period.
        Args: 
           freeblock: Looking  for time blocks in this period 
               that are not conflicting with appointments in 
               this agenda.
        Returns: 
           A new agenda containing exactly the times that 
           are within the period of freeblock and 
           not within appointments in this agenda. The 
           description of the resulting appointments comes
           from freeblock.desc.
        """
        copy = self.normalized()
        comp = Agenda()
        day = freeblock.begin.date()
        desc = freeblock.desc
        cur_time = freeblock.begin
        for appt in copy.appts:
            if appt < freeblock:
                continue
            if appt > freeblock:
                if cur_time < freeblock.end:
                    comp.append(Appt(day,cur_time.time(),freeblock.end.time(), desc))
                    cur_time = freeblock.end
                break
            if cur_time < appt.begin:
                # print("Creating free time from", cur_time, "to", appt.begin)
                comp.append(Appt(day, cur_time.time(), appt.begin.time(), desc))
            cur_time = max(appt.end,cur_time)
        if cur_time < freeblock.end:
            # print("Creating final free time from", cur_time, "to", freeblock.end)
            comp.append(Appt(day, cur_time.time(), freeblock.end.time(), desc))
        return comp



    def __len__(self):
        """Number of appointments, callable as built-in len() function"""
        return len(self.appts)

    def __iter__(self):
        """An iterator through the appointments in this agenda."""
        return self.appts.__iter__()

    def __str__(self):
        """String representation of a whole agenda"""
        rep = ""
        for appt in self.appts:
            rep += str(appt) + "\n"
        return rep[:-1]

    def __eq__(self,other):
        """Equality, ignoring descriptions --- just equal blocks of time"""
        if len(self.appts) != len(other.appts):
            return False
        for i in range(len(self.appts)):
            mine = self.appts[i]
            theirs = other.appts[i]
            if not (mine.begin == theirs.begin and
                    mine.end == theirs.end):
                return False
        return True