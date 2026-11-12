import csv
import os
from datetime import datetime

from src.data_reader import DataReader
from src.fleet_engine import FleetMonitoringEngine


FUEL_PRICE = 92
DATA_FOLDER = "data"

reader = DataReader()
vehicles = {}
zones = {}
gps_records = []
report_date = None


# =====================================
# 1. READ COMMAND FILE
# =====================================

command_file = os.path.join(DATA_FOLDER, "commands.txt")

if not os.path.exists(command_file):
    print("ERROR: commands.txt not found.")
    exit()

with open(command_file, "r", encoding="utf-8-sig") as file:
    commands = [
        line.strip()
        for line in file
        if line.strip() and not line.strip().startswith("#")
    ]


# =====================================
# 2. EXECUTE COMMANDS
# =====================================

for command in commands:

    parts = command.split("|")
    action = parts[0].strip()

    if action == "LOAD_ZONES":
        path = os.path.join(DATA_FOLDER, parts[1].strip())
        zones = reader.read_zones(path)

    elif action == "LOAD_VEHICLES":
        path = os.path.join(DATA_FOLDER, parts[1].strip())
        vehicles = reader.read_vehicles(path)

    elif action == "LOAD_PINGS":
        path = os.path.join(DATA_FOLDER, parts[1].strip())
        gps_records = reader.read_gps_data(path)

    elif action == "EVENT_LOG":
        print("Event log command received.")

    elif action == "DAILY_REPORT":
        report_date = parts[1].strip()


# =====================================
# 3. CREATE FLEET ENGINE
# =====================================

if not vehicles or not zones or not gps_records:
    print("ERROR: Required project data is missing.")
    exit()

engine = FleetMonitoringEngine(vehicles, zones)


# =====================================
# 4. PROCESS GPS RECORDS
# =====================================

print("\n===== PROCESSING OFFICIAL GPS DATA =====")

for ping in gps_records:
    engine.process_ping(ping)

events = engine.event_detector.events

print("\nTotal events detected:", len(events))


# =====================================
# 5. GENERATE EVENT LOG CSV
# =====================================

event_columns = [
    "vehicle_id",
    "event_type",
    "start_time",
    "end_time",
    "duration_min",
    "idle_cost_rs"
]

with open("event_log.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=event_columns)
    writer.writeheader()

    for event in sorted(events, key=lambda e: (e.vehicle_id, e.start_time)):

        end_time = event.end_time or ""
        duration = 0

        if end_time:
            start = datetime.strptime(event.start_time, "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            duration = int((end - start).total_seconds() / 60)

        idle_cost = 0.00

        if event.event_type == "IDLING" and duration > 0:
            vehicle = vehicles[event.vehicle_id]

            idle_cost = round(
                (duration / 60)
                * vehicle.idle_litres_per_hour
                * FUEL_PRICE,
                2
            )

        writer.writerow({
            "vehicle_id": event.vehicle_id,
            "event_type": event.event_type,
            "start_time": event.start_time,
            "end_time": end_time,
            "duration_min": duration,
            "idle_cost_rs": f"{idle_cost:.2f}"
        })


# =====================================
# 6. GENERATE DAILY REPORT CSV
# =====================================

report_columns = [
    "date",
    "vehicle_id",
    "driver_name",
    "geofence_events",
    "overspeed_events",
    "idling_events",
    "night_drive_events",
    "gps_lost_events",
    "idle_minutes",
    "idle_cost_rs",
    "driver_score"
]

penalties = {
    "GEOFENCE": 5,
    "OVERSPEED": 10,
    "IDLING": 2,
    "NIGHT_DRIVE": 15,
    "GPS_LOST": 0
}

with open("daily_report.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=report_columns)
    writer.writeheader()

    for vehicle_id in sorted(vehicles):

        vehicle = vehicles[vehicle_id]

        daily_events = [
            event for event in events
            if event.vehicle_id == vehicle_id
            and event.start_time[:10] == report_date
        ]

        counts = {
            event_type: sum(
                1 for event in daily_events
                if event.event_type == event_type
            )
            for event_type in penalties
        }

        idle_minutes = 0
        idle_cost = 0.0

        for event in daily_events:

            if event.event_type == "IDLING" and event.end_time:

                start = datetime.strptime(event.start_time, "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(event.end_time, "%Y-%m-%d %H:%M:%S")

                minutes = int((end - start).total_seconds() / 60)
                idle_minutes += minutes

                idle_cost += round(
                    (minutes / 60)
                    * vehicle.idle_litres_per_hour
                    * FUEL_PRICE,
                    2
                )

        score = max(
            0,
            100 - sum(
                counts[event_type] * penalties[event_type]
                for event_type in penalties
            )
        )

        writer.writerow({
            "date": report_date,
            "vehicle_id": vehicle_id,
            "driver_name": vehicle.driver_name,
            "geofence_events": counts["GEOFENCE"],
            "overspeed_events": counts["OVERSPEED"],
            "idling_events": counts["IDLING"],
            "night_drive_events": counts["NIGHT_DRIVE"],
            "gps_lost_events": counts["GPS_LOST"],
            "idle_minutes": idle_minutes,
            "idle_cost_rs": f"{idle_cost:.2f}",
            "driver_score": score
        })


# =====================================
# 7. GENERATE ERRORS CSV
# =====================================

all_errors = []

all_errors.extend(reader.errors)
all_errors.extend(engine.errors)
all_errors.extend(engine.gps_processor.errors)

all_errors.sort(key=lambda error: int(error["line_no"]))

error_columns = [
    "line_no",
    "ping_id",
    "vehicle_id",
    "reason"
]

with open("errors.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=error_columns)
    writer.writeheader()
    writer.writerows(all_errors)


# =====================================
# 8. FINAL MESSAGE
# =====================================

print("\nTotal rejected records:", len(all_errors))

print("\n===== PROJECT COMPLETED =====")
print("Event log saved: event_log.csv")
print("Daily report saved: daily_report.csv")
print("Errors saved: errors.csv")
print("Report date:", report_date)