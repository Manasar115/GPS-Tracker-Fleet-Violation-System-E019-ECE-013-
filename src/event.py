class Event:

    def __init__(self, event_type, vehicle_id, start_time):

        self.event_type = event_type
        self.vehicle_id = vehicle_id
        self.start_time = start_time
        self.end_time = None

    def close_event(self, end_time):

        self.end_time = end_time

    def display_event(self):

        print("Event Type:", self.event_type)
        print("Vehicle ID:", self.vehicle_id)
        print("Start Time:", self.start_time)
        print("End Time:", self.end_time)