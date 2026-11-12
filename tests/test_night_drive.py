import unittest

from src.event_detector import EventDetector
from src.gps_ping import GPSPing


class TestNightDrive(unittest.TestCase):

    def setUp(self):
        self.detector = EventDetector()

    def create_ping(self, timestamp, speed):

        return GPSPing(
            "V001",
            timestamp,
            13.00,
            77.60,
            speed,
            "ON"
        )

    def test_night_driving_detection(self):

        ping = self.create_ping(
            "2026-11-07 23:00", 40
        )

        self.detector.detect_night_drive(ping)

        self.assertEqual(len(self.detector.events), 1)

        self.assertEqual(
            self.detector.events[0].event_type,
            "NIGHT_DRIVE"
        )

    def test_night_event_closes_after_five_stopped_pings(self):

        # Start night driving
        ping = self.create_ping(
            "2026-11-07 23:00", 40
        )

        self.detector.detect_night_drive(ping)

        # Five consecutive stopped readings
        for minute in range(1, 6):

            ping = self.create_ping(
                f"2026-11-07 23:0{minute}", 0
            )

            self.detector.detect_night_drive(ping)

        self.assertEqual(
            self.detector.events[0].end_time,
            "2026-11-07 23:05"
        )

    def test_movement_before_eleven_pm(self):

        # Vehicle starts moving at 10:59 PM
        first_ping = self.create_ping(
            "2026-11-07 22:59", 40
        )

        self.detector.detect_night_drive(first_ping)

        # No night-driving event should exist yet
        self.assertEqual(len(self.detector.events), 0)

        # Vehicle continues moving at 11:00 PM
        second_ping = self.create_ping(
            "2026-11-07 23:00", 40
        )

        self.detector.detect_night_drive(second_ping)

        # Night-driving event should start at 11:00 PM
        self.assertEqual(len(self.detector.events), 1)

        self.assertEqual(
            self.detector.events[0].start_time,
            "2026-11-07 23:00"
        )


if __name__ == "__main__":
    unittest.main()