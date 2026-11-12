from src.gps_processor import GPSProcessor
from src.event_detector import EventDetector


class FleetMonitoringEngine:

    def __init__(self, vehicles, zones):

        self.vehicles = vehicles
        self.zones = zones

        # Create GPS processor
        self.gps_processor = GPSProcessor()

        # Create event detector
        self.event_detector = EventDetector()

        # Store rejected GPS records
        self.errors = []

    def process_ping(self, ping):

        vehicle_id = ping.vehicle_id
        line_no = getattr(ping, "line_no", "")

        # Check whether vehicle exists
        if vehicle_id not in self.vehicles:

            reason = "Unknown vehicle"
            print("ERROR:", reason + ":", vehicle_id)

            self.errors.append({
                "line_no": line_no,
                "ping_id": ping.ping_id,
                "vehicle_id": vehicle_id,
                "reason": reason
            })

            return False

        vehicle = self.vehicles[vehicle_id]

        # Check whether assigned zone exists
        if vehicle.zone_id not in self.zones:

            reason = "Unknown zone"
            print("ERROR:", reason + ":", vehicle.zone_id)

            self.errors.append({
                "line_no": line_no,
                "ping_id": ping.ping_id,
                "vehicle_id": vehicle_id,
                "reason": reason
            })

            return False

        zone = self.zones[vehicle.zone_id]

        # Validate GPS record and timestamp order
        if not self.gps_processor.process_ping(ping):
            return False

        # Detect GPS signal loss
        self.event_detector.detect_gps_loss(ping)

        # Detect all other events
        self.event_detector.detect_geofence(ping, zone)

        self.event_detector.detect_overspeed(ping, vehicle)

        self.event_detector.detect_idling(ping)

        self.event_detector.detect_night_drive(ping)

        return True