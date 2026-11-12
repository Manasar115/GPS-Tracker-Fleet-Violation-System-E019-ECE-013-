import unittest
from io import StringIO
from contextlib import redirect_stdout

from src.fleet_report import FleetReport
from src.vehicle import Vehicle
from src.event import Event


class TestFleetReport(unittest.TestCase):

    def setUp(self):

        self.report = FleetReport()

        self.vehicles = {
            "V001": Vehicle(
                "V001", "D001", "Z001", 50, 2.5
            )
        }

        self.events = [
            Event(
                "OVERSPEED",
                "V001",
                "2026-11-07 10:00"
            )
        ]

    def test_event_log_display(self):

        output = StringIO()

        with redirect_stdout(output):

            self.report.display_event_log(
                self.events
            )

        result = output.getvalue()

        self.assertIn("OVERSPEED", result)
        self.assertIn("V001", result)

    def test_daily_report_display(self):

        output = StringIO()

        with redirect_stdout(output):

            self.report.display_daily_report(
                "2026-11-07",
                self.vehicles,
                self.events,
                {"D001": 90},
                {"V001": 46.0}
            )

        result = output.getvalue()

        self.assertIn("V001", result)
        self.assertIn("D001", result)
        self.assertIn("90", result)
        self.assertIn("46.0", result)
        self.assertIn("Total Violations: 1", result)


if __name__ == "__main__":
    unittest.main()
    