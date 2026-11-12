import unittest

from src.event_detector import EventDetector
from src.gps_ping import GPSPing


class TestIdling(unittest.TestCase):

    def setUp(self):
        self.detector = EventDetector()

    def create_ping(self, minute, speed=0, ignition="ON"):

        return GPSPing(
            "V001",
            f"2026-11-07 10:{minute:02d}",
            13.00,
            77.60,
            speed,
            ignition
        )

    def test_exactly_ten_minutes(self):

        # 10:00 to 10:10 = exactly 10 minutes
        for minute in range(11):
            ping = self.create_ping(minute)
            self.detector.detect_idling(ping)

        self.assertEqual(len(self.detector.events), 0)

    def test_more_than_ten_minutes(self):

        # 10:00 to 10:11 = 11 minutes
        for minute in range(12):
            ping = self.create_ping(minute)
            self.detector.detect_idling(ping)

        self.assertEqual(len(self.detector.events), 1)

        self.assertEqual(
            self.detector.events[0].event_type,
            "IDLING"
        )

        self.assertEqual(
            self.detector.events[0].start_time,
            "2026-11-07 10:00"
        )

    def test_ignition_off(self):

        for minute in range(12):
            ping = self.create_ping(minute, 0, "OFF")
            self.detector.detect_idling(ping)

        self.assertEqual(len(self.detector.events), 0)


if __name__ == "__main__":
    unittest.main()