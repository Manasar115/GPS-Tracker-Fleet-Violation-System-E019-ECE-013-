class FleetReport:

    def display_event_log(self, events):

        print("\n========== EVENT LOG ==========")

        if not events:
            print("No events detected.")
            return

        for event in events:

            print("------------------------------")
            print("Event Type:", event.event_type)
            print("Vehicle ID:", event.vehicle_id)
            print("Start Time:", event.start_time)
            print("End Time:", event.end_time)

    def display_daily_report(
        self, date, vehicles, events, daily_scores, idling_costs
    ):

        print("\n========== DAILY FLEET REPORT ==========")
        print("Report Date:", date)

        if not vehicles:
            print("No vehicles registered.")
            return

        for vehicle_id, vehicle in vehicles.items():

            driver_id = getattr(
                vehicle, "driver_id", vehicle.driver_name
            )

            print("\n--------------------------------")
            print("Vehicle ID:", vehicle_id)
            print("Driver ID:", driver_id)

            violation_count = 0

            for event in events:

                if event.vehicle_id == vehicle_id:
                    if event.start_time[:10] == date:
                        violation_count += 1

            print("Total Violations:", violation_count)

            cost = idling_costs.get(vehicle_id, 0.0)
            print("Idling Fuel Cost: Rs.", cost)

            score = daily_scores.get(driver_id, 100)
            print("Daily Driver Score:", score)

        print("\n========================================")
        print("END OF DAILY FLEET REPORT")
        print("========================================")