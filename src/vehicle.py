class Vehicle:

    def __init__(
        self,
        vehicle_id,
        registration_no,
        driver_name=None,
        driver_mobile=None,
        zone_id=None,
        speed_limit_kmph=None,
        idle_litres_per_hour=None
    ):

        # Support older 5-argument constructor
        if idle_litres_per_hour is None:
            old_driver_id = registration_no
            old_zone_id = driver_name
            old_speed_limit = driver_mobile
            old_idle_rate = zone_id

            registration_no = ""
            driver_name = old_driver_id
            driver_mobile = ""
            zone_id = old_zone_id
            speed_limit_kmph = old_speed_limit
            idle_litres_per_hour = old_idle_rate

        self.vehicle_id = vehicle_id
        self.registration_no = registration_no
        self.driver_name = driver_name or ""
        self.driver_id = self.driver_name
        self.driver_mobile = str(driver_mobile or "")
        self.zone_id = zone_id

        self.speed_limit_kmph = float(speed_limit_kmph)
        self.idle_litres_per_hour = float(idle_litres_per_hour)

        # Compatibility aliases
        self.speed_limit = self.speed_limit_kmph
        self.idle_fuel_rate = self.idle_litres_per_hour

    def get_vehicle_details(self):
        print("Vehicle ID:", self.vehicle_id)
        print("Registration Number:", self.registration_no)
        print("Driver Name:", self.driver_name)
        print("Driver Mobile:", self.driver_mobile)
        print("Zone ID:", self.zone_id)
        print("Speed Limit:", self.speed_limit_kmph, "km/h")
        print("Idle Fuel Rate:", self.idle_litres_per_hour, "L/hour")