import unittest

from src.event_detector import EventDetector
from src.gps_ping import GPSPing


class TestGPSLoss(unittest.TestCase):

    def setUp(self):
        self.detector = EventDetector()

    def create_ping(self, timestamp):

        return GPSPing(
            "V001",
            timestamp,
            13.00,
            77.60,
            40,
            "ON"
        )

    def test_exactly_fifteen_minutes(self):

        first_ping = self.create_ping(
            "2026-11-07 10:00"
        )

        second_ping = self.create_ping(
            "2026-11-07 10:15"
        )

        self.detector.detect_gps_loss(first_ping)
        self.detector.detect_gps_loss(second_ping)

        self.assertEqual(len(self.detector.events), 0)

    def test_more_than_fifteen_minutes(self):

        first_ping = self.create_ping(
            "2026-11-07 10:00"
        )

        second_ping = self.create_ping(
            "2026-11-07 10:16"
        )

        self.detector.detect_gps_loss(first_ping)
        self.detector.detect_gps_loss(second_ping)

        self.assertEqual(len(self.detector.events), 1)

        self.assertEqual(
            self.detector.events[0].event_type,
            "GPS_LOST"
        )

    def test_gps_loss_resets_consecutive_counters(self):

        first_ping = self.create_ping(
            "2026-11-07 10:00"
        )

        # Store the first GPS timestamp
        self.detector.detect_gps_loss(first_ping)

        # Simulate consecutive detection counters
        self.detector.outside_count["V001"] = 2
        self.detector.overspeed_count["V001"] = 2
        self.detector.idling_count["V001"] = 5
        self.detector.night_stop_count["V001"] = 3

        # Simulate stored starting timestamps
        self.detector.first_outside_time["V001"] = "10:01"
        self.detector.first_overspeed_time["V001"] = "10:02"
        self.detector.first_idling_time["V001"] = "10:03"

        # More than 15 minutes later
        second_ping = self.create_ping(
            "2026-11-07 10:16"
        )

        self.detector.detect_gps_loss(second_ping)

        # Check that all consecutive counters are reset
        self.assertEqual(self.detector.outside_count["V001"], 0)
        self.assertEqual(self.detector.overspeed_count["V001"], 0)
        self.assertEqual(self.detector.idling_count["V001"], 0)
        self.assertEqual(self.detector.night_stop_count["V001"], 0)

        # Check that starting timestamps are cleared
        self.assertNotIn("V001", self.detector.first_outside_time)
        self.assertNotIn("V001", self.detector.first_overspeed_time)
        self.assertNotIn("V001", self.detector.first_idling_time)


if __name__ == "__main__":
    unittest.main()