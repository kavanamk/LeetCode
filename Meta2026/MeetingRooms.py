from collections import defaultdict
class MeetingScheduler:
    def __init__(self):
        self.meetings=defaultdict(list)

    # ─── LEVEL 1 ─────────────────────────────────────────────────────────────
    def book(self, start: int, end: int, room_id: int) -> None:
        """
        Inputs:  start   (int) — meeting start time (inclusive)
                 end     (int) — meeting end time (exclusive)
                 room_id (int) — the room being booked
        Output:  None
        Does:    Records a meeting in room_id from start to end.
                 Assume all bookings are valid (no overlap checking needed here).
        """
        self.meetings[room_id].append((start,end))

    def get_meetings(self, room_id: int) -> list:
        """
        Input:   room_id (int)
        Output:  List of (start, end) tuples for all meetings in that room,
                 sorted by start time. Returns [] if room has no meetings.
        Does:    Returns all scheduled meetings for a given room.
        """
        return sorted(self.meetings[room_id])

    # ─── LEVEL 2 ─────────────────────────────────────────────────────────────
    def is_available(self, start: int, end: int, room_id: int) -> bool:
        """
        Inputs:  start, end (int) — the time slot to check
                 room_id    (int) — the room to check
        Output:  bool — True if room_id has no bookings that overlap
                 [start, end), False otherwise.
        Does:    Checks whether a room is free for the entire requested slot.
                 Two meetings overlap if one starts before the other ends.
        """
        meetingTimes = self.get_meetings(room_id)
        #find the position of start and end
        #chcek if start date is<end date false!
        if (start,end) not in meetingTimes:
            meetingTimes.append((start, end))
            meetingTimes.sort(key=lambda x: x[0])
        idx=meetingTimes.index((start,end))

        if idx>0:
            prev=meetingTimes[idx-1]
            prev_star,prev_end=prev
            if start <prev_end:
                return False
        if idx<len(meetingTimes)-1:
            nxt = meetingTimes[idx+1]
            nxt_start,nxt_end=nxt
            if end>nxt_start:
                return False
        return True

        #brute force recommended by claude
        # for s, e in self.meetings[room_id]:
        #     if s < end and e > start:
        #         return False
        # return True




    # ─── LEVEL 3 ─────────────────────────────────────────────────────────────
    def min_rooms(self, meetings: list) -> int:  # noqa
        """
        Input:   meetings (List of [start, end] pairs) — a list of meetings
                 that all need to be scheduled simultaneously.
        Output:  int — the minimum number of rooms required to hold all
                 meetings with no overlaps.
        Does:    Given a set of meetings, finds the fewest rooms needed so
                 that no two overlapping meetings share a room.
        Example: [[0,30],[5,10],[15,20]] needs 2 rooms.
        """
        meetings.sort(key=lambda x:x[0])
        startTimes=sorted([x for x,y in meetings])
        endTimes=sorted([y for x,y in meetings])
        i, j = 0, 0
        rooms = 0
        max_rooms = 0
        while i < len(startTimes):
            if startTimes[i] < endTimes[j]:  # new meeting starts before earliest end → need a room
                rooms += 1
                i += 1
            else:                             # a meeting ended → free a room
                rooms -= 1
                j += 1
            max_rooms = max(max_rooms, rooms)
        return max_rooms

    # ─── LEVEL 4 ─────────────────────────────────────────────────────────────
    def busiest_period(self) -> tuple:
        """
        Input:   None
        Output:  (start, end, count) tuple — the time interval during which
                 the most rooms are simultaneously in use, and how many.
                 If multiple periods tie, return the earliest one.
        Does:    Across all booked meetings, finds the moment of peak
                 concurrent room usage and returns the interval and count.
        Example: meetings [(1,5), (2,4), (3,7)] → peak is (3,4) with 3 rooms.
        """
        pass
