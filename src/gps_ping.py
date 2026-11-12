from datetime import datetime
import math


class GPSPing:
    def __init__(
        self,
        ping_id=None,
        vehicle_id=None,
        timestamp=None,
        latitude=None,
        longitude=None,
        speed_kmph=None,
        ignition=None
    ):

        # Support older 6-argument constructor
        if ignition is None:
            old_vehicle_id = ping_id
            old_timestamp = vehicle_id
            old_latitude = timestamp
            old_longitude = latitude
            old_speed = longitude
            old_ignition = speed_kmph

            ping_id = old_vehicle_id
            vehicle_id = old_vehicle_id
            timestamp = old_timestamp
            latitude = old_latitude
            longitude = old_longitude
            speed_kmph = old_speed
            ignition = old_ignition

        self.ping_id = ping_id
        self.vehicle_id = vehicle_id
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.speed_kmph = speed_kmph
        self.ignition = ignition

        self.speed = self.speed_kmph
        self.ignition_status = self.ignition

    def validate_ping(self):
        if not self.ping_id or not self.vehicle_id:
            return False

        valid_timestamp = False

        for time_format in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M"
        ):
            try:
                datetime.strptime(self.timestamp, time_format)
                valid_timestamp = True
                break
            except (ValueError, TypeError):
                pass

        if not valid_timestamp:
            return False

        try:
            latitude = float(self.latitude)
            longitude = float(self.longitude)
            speed = float(self.speed_kmph)
        except (ValueError, TypeError):
            return False

        if not all(map(math.isfinite, [latitude, longitude, speed])):
            return False

        if not -90 <= latitude <= 90:
            return False

        if not -180 <= longitude <= 180:
            return False

        if speed < 0:
            return False

        if self.ignition not in ["ON", "OFF"]:
            return False

        return True