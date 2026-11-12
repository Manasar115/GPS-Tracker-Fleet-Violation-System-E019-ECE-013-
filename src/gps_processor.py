from datetime import datetime


class GPSProcessor:

    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
    OLD_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"

    def __init__(self):
        self.last_timestamp = {}
        self.errors = []

    def parse_timestamp(self, timestamp):

        for fmt in (self.TIMESTAMP_FORMAT, self.OLD_TIMESTAMP_FORMAT):
            try:
                return datetime.strptime(timestamp, fmt)
            except (ValueError, TypeError):
                pass

        raise ValueError("Invalid timestamp")

    def validate_data(self, ping):

        if not ping.validate_ping():
            return False

        try:
            current_time = self.parse_timestamp(ping.timestamp)
        except ValueError:
            return False

        vehicle_id = ping.vehicle_id

        if vehicle_id in self.last_timestamp:
            if current_time <= self.last_timestamp[vehicle_id]:
                return False

        self.last_timestamp[vehicle_id] = current_time
        return True

    def process_ping(self, ping):

        vehicle_id = ping.vehicle_id
        line_no = getattr(ping, "line_no", "")

        if not ping.validate_ping():
            reason = "Invalid GPS record"
            print("ERROR:", reason + ":", ping.ping_id)

            self.errors.append({
                "line_no": line_no,
                "ping_id": ping.ping_id,
                "vehicle_id": vehicle_id,
                "reason": reason
            })

            return False

        try:
            current_time = self.parse_timestamp(ping.timestamp)

        except ValueError:
            reason = "Invalid timestamp"
            print("ERROR:", reason + ":", ping.ping_id)

            self.errors.append({
                "line_no": line_no,
                "ping_id": ping.ping_id,
                "vehicle_id": vehicle_id,
                "reason": reason
            })

            return False

        if vehicle_id in self.last_timestamp:

            previous_time = self.last_timestamp[vehicle_id]

            if current_time <= previous_time:
                reason = "Out-of-order GPS record"
                print("ERROR:", reason + ":", ping.ping_id)

                self.errors.append({
                    "line_no": line_no,
                    "ping_id": ping.ping_id,
                    "vehicle_id": vehicle_id,
                    "reason": reason
                })

                return False

        self.last_timestamp[vehicle_id] = current_time
        return True