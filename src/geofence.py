class GeofenceZone:
    def __init__(
        self,
        zone_id,
        zone_name,
        min_latitude,
        max_latitude,
        min_longitude=None,
        max_longitude=None
    ):

        # Support older 5-argument constructor
        if max_longitude is None:
            old_min_latitude = zone_name
            old_max_latitude = min_latitude
            old_min_longitude = max_latitude
            old_max_longitude = min_longitude

            zone_name = zone_id
            min_latitude = old_min_latitude
            max_latitude = old_max_latitude
            min_longitude = old_min_longitude
            max_longitude = old_max_longitude

        self.zone_id = zone_id
        self.zone_name = zone_name

        self.min_latitude = float(min_latitude)
        self.max_latitude = float(max_latitude)
        self.min_longitude = float(min_longitude)
        self.max_longitude = float(max_longitude)

    def is_inside_zone(self, latitude, longitude):
        return (
            self.min_latitude <= latitude <= self.max_latitude
            and self.min_longitude <= longitude <= self.max_longitude
        )