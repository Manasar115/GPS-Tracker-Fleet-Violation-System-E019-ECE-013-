from datetime import datetime


class CostCalculator:

    FUEL_PRICE_PER_LITRE = 92

    def calculate_idling_cost(self, event, vehicle):

        # Check whether this is an idling event
        if event.event_type != "IDLING":
            return 0.0

        # Check whether the event has ended
        if event.end_time is None:
            return 0.0

        # Convert timestamps into datetime format
        start_time = datetime.strptime(
            event.start_time, "%Y-%m-%d %H:%M"
        )

        end_time = datetime.strptime(
            event.end_time, "%Y-%m-%d %H:%M"
        )

        # Calculate total idling duration
        idle_minutes = (
            end_time - start_time
        ).total_seconds() / 60

        # Calculate fuel consumed
        fuel_used = (
            idle_minutes / 60
        ) * vehicle.idle_fuel_rate

        # Calculate total fuel cost
        total_cost = (
            fuel_used * self.FUEL_PRICE_PER_LITRE
        )

        return round(total_cost, 2)