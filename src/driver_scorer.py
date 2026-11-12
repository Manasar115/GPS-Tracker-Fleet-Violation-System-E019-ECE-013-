class DriverScorer:

    PENALTIES = {
        "GEOFENCE": 5,
        "OVERSPEED": 10,
        "IDLING": 2,
        "NIGHT_DRIVE": 15,
        "GPS_LOST": 0
    }

    def calculate_daily_score(self, driver_id, date, events, vehicles):

        score = 100

        for event in events:

            vehicle = vehicles.get(event.vehicle_id)

            if vehicle is None:
                continue

            vehicle_driver_id = getattr(
                vehicle, "driver_id",
                getattr(vehicle, "driver_name", None)
            )

            if vehicle_driver_id != driver_id:
                continue

            if event.start_time[:10] != date:
                continue

            penalty = self.PENALTIES.get(event.event_type, 0)

            score -= penalty

        return max(0, score)