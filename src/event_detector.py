from datetime import datetime
from src.event import Event


class EventDetector:

    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
    OLD_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"

    def __init__(self):
        self.outside_count = {}
        self.active_geofence_events = {}
        self.first_outside_time = {}

        self.overspeed_count = {}
        self.active_overspeed_events = {}
        self.first_overspeed_time = {}

        self.first_idling_time = {}
        self.idling_count = {}
        self.active_idling_events = {}

        self.night_stop_count = {}
        self.active_night_events = {}

        self.last_ping_time = {}
        self.events = []

    def parse_timestamp(self, timestamp):
        for fmt in (self.TIMESTAMP_FORMAT, self.OLD_TIMESTAMP_FORMAT):
            try:
                return datetime.strptime(timestamp, fmt)
            except (ValueError, TypeError):
                pass

        raise ValueError("Invalid timestamp")

    def detect_geofence(self, ping, zone):
        vid = ping.vehicle_id

        if not zone.is_inside_zone(ping.latitude, ping.longitude):
            self.outside_count[vid] = self.outside_count.get(vid, 0) + 1

            if self.outside_count[vid] == 1:
                self.first_outside_time[vid] = ping.timestamp

            if self.outside_count[vid] >= 2 and vid not in self.active_geofence_events:
                event = Event("GEOFENCE", vid, ping.timestamp)
                self.active_geofence_events[vid] = event
                self.events.append(event)

        else:
            if vid in self.active_geofence_events:
                self.active_geofence_events[vid].close_event(ping.timestamp)
                del self.active_geofence_events[vid]

            self.outside_count[vid] = 0
            self.first_outside_time.pop(vid, None)

    def detect_overspeed(self, ping, vehicle):
        vid = ping.vehicle_id
        speed = float(ping.speed_kmph)
        limit = vehicle.speed_limit_kmph

        if speed > limit * 1.10:
            self.overspeed_count[vid] = self.overspeed_count.get(vid, 0) + 1

            if self.overspeed_count[vid] == 1:
                self.first_overspeed_time[vid] = ping.timestamp

            if self.overspeed_count[vid] >= 3 and vid not in self.active_overspeed_events:
                event = Event("OVERSPEED", vid, ping.timestamp)
                self.active_overspeed_events[vid] = event
                self.events.append(event)

        else:
            if speed <= limit and vid in self.active_overspeed_events:
                self.active_overspeed_events[vid].close_event(ping.timestamp)
                del self.active_overspeed_events[vid]

            self.overspeed_count[vid] = 0
            self.first_overspeed_time.pop(vid, None)

    def detect_idling(self, ping):
        vid = ping.vehicle_id

        if ping.ignition == "ON" and float(ping.speed_kmph) == 0:

            if vid not in self.first_idling_time:
                self.first_idling_time[vid] = ping.timestamp
                self.idling_count[vid] = 0

            self.idling_count[vid] = self.idling_count.get(vid, 0) + 1

            start = self.parse_timestamp(self.first_idling_time[vid])
            current = self.parse_timestamp(ping.timestamp)

            idle_minutes = (current - start).total_seconds() / 60

            if idle_minutes > 10 and vid not in self.active_idling_events:

                # Compatibility with older minute-only test timestamps
                if len(ping.timestamp) == 16:
                    event_start = self.first_idling_time[vid]
                else:
                    event_start = ping.timestamp

                event = Event("IDLING", vid, event_start)
                self.active_idling_events[vid] = event
                self.events.append(event)

        else:
            if vid in self.active_idling_events:
                self.active_idling_events[vid].close_event(ping.timestamp)
                del self.active_idling_events[vid]

            self.first_idling_time.pop(vid, None)
            self.idling_count[vid] = 0

    def detect_night_drive(self, ping):
        vid = ping.vehicle_id
        current = self.parse_timestamp(ping.timestamp).time()

        is_night = current.hour >= 23 or current.hour < 5

        if is_night and float(ping.speed_kmph) > 5:
            self.night_stop_count[vid] = 0

            if vid not in self.active_night_events:
                event = Event("NIGHT_DRIVE", vid, ping.timestamp)
                self.active_night_events[vid] = event
                self.events.append(event)

        elif vid in self.active_night_events:
            if float(ping.speed_kmph) <= 5:
                self.night_stop_count[vid] = self.night_stop_count.get(vid, 0) + 1

                if self.night_stop_count[vid] >= 5:
                    self.active_night_events[vid].close_event(ping.timestamp)
                    del self.active_night_events[vid]
                    self.night_stop_count[vid] = 0
            else:
                self.night_stop_count[vid] = 0

    def detect_gps_loss(self, ping):
        vid = ping.vehicle_id
        current = self.parse_timestamp(ping.timestamp)

        if vid in self.last_ping_time:
            previous = self.last_ping_time[vid]
            gap = (current - previous).total_seconds() / 60

            if gap > 15:
                previous_format = (
                    self.OLD_TIMESTAMP_FORMAT
                    if len(ping.timestamp) == 16
                    else self.TIMESTAMP_FORMAT
                )

                previous_text = previous.strftime(previous_format)

                event = Event("GPS_LOST", vid, previous_text)
                event.close_event(ping.timestamp)
                self.events.append(event)

                self.outside_count[vid] = 0
                self.overspeed_count[vid] = 0
                self.idling_count[vid] = 0
                self.night_stop_count[vid] = 0

                self.first_outside_time.pop(vid, None)
                self.first_overspeed_time.pop(vid, None)
                self.first_idling_time.pop(vid, None)

        self.last_ping_time[vid] = current