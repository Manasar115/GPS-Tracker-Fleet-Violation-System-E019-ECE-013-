import unittest

from src.driver_scorer import DriverScorer
from src.event import Event
from src.vehicle import Vehicle


class TestDriverScorer(unittest.TestCase):

    def setUp(self):

        self.scorer = DriverScorer()

        self.vehicles = {
            "V001": Vehicle(
                "V001", "D001", "Z001", 50, 2.5
            )
        }

    def test_daily_score_calculation(self):

        events = [
            Event("GEOFENCE", "V001", "2026-11-07 10:00"),
            Event("OVERSPEED", "V001", "2026-11-07 10:05"),
            Event("IDLING", "V001", "2026-11-07 10:10"),
            Event("NIGHT_DRIVE", "V001", "2026-11-07 23:00"),
            Event("GPS_LOST", "V001", "2026-11-07 23:30")
        ]

        score = self.scorer.calculate_daily_score(
            "D001",
            "2026-11-07",
            events,
            self.vehicles
        )

        self.assertEqual(score, 68)

    def test_score_cannot_be_negative(self):

        events = []

        for i in range(15):
            events.append(
                Event(
                    "OVERSPEED",
                    "V001",
                    "2026-11-07 10:00"
                )
            )

        score = self.scorer.calculate_daily_score(
            "D001",
            "2026-11-07",
            events,
            self.vehicles
        )

        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()