import unittest

from src.geofence import GeofenceZone


class TestGeofence(unittest.TestCase):

    def setUp(self):

        self.zone = GeofenceZone(
            "Z001",
            12.90,
            13.10,
            77.50,
            77.70
        )

    def test_location_inside_zone(self):

        result = self.zone.is_inside_zone(13.00, 77.60)

        self.assertTrue(result)

    def test_location_outside_zone(self):

        result = self.zone.is_inside_zone(13.50, 78.00)

        self.assertFalse(result)

    def test_boundary_location(self):

        result = self.zone.is_inside_zone(13.10, 77.70)

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()