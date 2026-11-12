import unittest

from src.cost_calculator import CostCalculator
from src.event import Event
from src.vehicle import Vehicle


class TestCostCalculator(unittest.TestCase):

    def setUp(self):

        self.calculator = CostCalculator()

        self.vehicle = Vehicle(
            "V001", "D001", "Z001", 50, 2.5
        )

    def test_idling_cost_calculation(self):

        event = Event(
            "IDLING",
            "V001",
            "2026-11-07 10:00"
        )

        event.close_event("2026-11-07 10:20")

        cost = self.calculator.calculate_idling_cost(
            event,
            self.vehicle
        )

        self.assertEqual(cost, 76.67)

    def test_non_idling_event_cost(self):

        event = Event(
            "OVERSPEED",
            "V001",
            "2026-11-07 10:00"
        )

        event.close_event("2026-11-07 10:20")

        cost = self.calculator.calculate_idling_cost(
            event,
            self.vehicle
        )

        self.assertEqual(cost, 0.0)

    def test_unclosed_idling_event_cost(self):

        event = Event(
            "IDLING",
            "V001",
            "2026-11-07 10:00"
        )

        cost = self.calculator.calculate_idling_cost(
            event,
            self.vehicle
        )

        self.assertEqual(cost, 0.0)


if __name__ == "__main__":
    unittest.main()