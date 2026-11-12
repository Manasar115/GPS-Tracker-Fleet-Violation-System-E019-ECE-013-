import unittest

from src.gps_ping import GPSPing
from src.gps_processor import GPSProcessor


class TestGPSValidation(unittest.TestCase):

    def setUp(self):
        self.processor = GPSProcessor()

    def test_valid_gps_record(self):

        ping = GPSPing(
            "V001",
            "2026-11-07 10:00",
            13.00,
            77.60,
            40,
            "ON"
        )

        self.assertTrue(self.processor.validate_data(ping))

    def test_invalid_latitude(self):

        ping = GPSPing(
            "V001",
            "2026-11-07 10:00",
            150.00,
            77.60,
            40,
            "ON"
        )

        self.assertFalse(self.processor.validate_data(ping))

    def test_out_of_order_timestamp(self):

        first_ping = GPSPing(
            "V001",
            "2026-11-07 10:05",
            13.00,
            77.60,
            40,
            "ON"
        )

        second_ping = GPSPing(
            "V001",
            "2026-11-07 10:03",
            13.00,
            77.60,
            40,
            "ON"
        )

        self.assertTrue(self.processor.validate_data(first_ping))
        self.assertFalse(self.processor.validate_data(second_ping))

    def test_nan_latitude(self):

        ping = GPSPing(
            "V001",
            "2026-11-07 10:00",
            float("nan"),
            77.60,
            40,
            "ON"
        )

        self.assertFalse(self.processor.validate_data(ping))

    def test_infinite_longitude(self):

        ping = GPSPing(
            "V001",
            "2026-11-07 10:00",
            13.00,
            float("inf"),
            40,
            "ON"
        )

        self.assertFalse(self.processor.validate_data(ping))

    def test_infinite_speed(self):

        ping = GPSPing(
            "V001",
            "2026-11-07 10:00",
            13.00,
            77.60,
            float("inf"),
            "ON"
        )

        self.assertFalse(self.processor.validate_data(ping))

    def test_empty_vehicle_id(self):

        ping = GPSPing(
            "",
            "2026-11-07 10:00",
            13.00,
            77.60,
            40,
            "ON"
        )

        self.assertFalse(self.processor.validate_data(ping))


if __name__ == "__main__":
    unittest.main()