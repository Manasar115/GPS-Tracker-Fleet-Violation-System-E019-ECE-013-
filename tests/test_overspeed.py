import unittest

from src.event_detector import EventDetector
from src.vehicle import Vehicle
from src.gps_ping import GPSPing


class TestOverspeed(unittest.TestCase):

    def setUp(self):

        self.detector = EventDetector()

        self.vehicle = Vehicle(
            "V001", "D001", "Z001", 50, 2.5
        )

    def create_ping(self, timestamp, speed):

        return GPSPing(
            "V001",
            timestamp,
            13.00,
            77.60,
            speed,
            "ON"
        )

    def test_overspeed_detection(self):

        speeds = [56, 60, 65]

        for minute, speed in enumerate(speeds, start=1):

            ping = self.create_ping(
                f"2026-11-07 10:0{minute}",
                speed
            )

            self.detector.detect_overspeed(
                ping, self.vehicle
            )

        self.assertEqual(len(self.detector.events), 1)

        self.assertEqual(
            self.detector.events[0].event_type,
            "OVERSPEED"
        )

    def test_exact_ten_percent_above_limit(self):

        ping = self.create_ping(
            "2026-11-07 10:01",
            55
        )

        self.detector.detect_overspeed(
            ping, self.vehicle
        )

        self.assertEqual(len(self.detector.events), 0)

    def test_overspeed_event_closes_at_speed_limit(self):

        # Three consecutive readings above 55 km/h
        speeds = [56, 56, 56]

        for minute, speed in enumerate(speeds, start=1):

            ping = self.create_ping(
                f"2026-11-07 10:0{minute}",
                speed
            )

            self.detector.detect_overspeed(
                ping, self.vehicle
            )

        # Event should now be active
        self.assertEqual(len(self.detector.events), 1)

        # Speed 55 is above the actual speed limit.
        # The event must remain open.
        ping = self.create_ping(
            "2026-11-07 10:04", 55
        )

        self.detector.detect_overspeed(
            ping, self.vehicle
        )

        self.assertIsNone(
            self.detector.events[0].end_time
        )

        # Speed returns to 50 km/h.
        # The event should close.
        ping = self.create_ping(
            "2026-11-07 10:05", 50
        )

        self.detector.detect_overspeed(
            ping, self.vehicle
        )

        self.assertEqual(
            self.detector.events[0].end_time,
            "2026-11-07 10:05"
        )


if __name__ == "__main__":
    unittest.main()