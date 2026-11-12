import csv
from src.gps_ping import GPSPing
from src.vehicle import Vehicle
from src.geofence import GeofenceZone


class DataReader:

    REQUIRED_COLUMNS = [
        "ping_id", "vehicle_id", "timestamp",
        "latitude", "longitude", "speed_kmph", "ignition"
    ]

    def __init__(self):
        self.errors = []

    def read_vehicles(self, file_path):
        vehicles = {}

        try:
            with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                required = [
                    "vehicle_id", "registration_no", "driver_name",
                    "driver_mobile", "zone_id", "speed_limit_kmph",
                    "idle_litres_per_hour"
                ]

                if not reader.fieldnames or not all(
                    column in reader.fieldnames for column in required
                ):
                    print("ERROR: Invalid vehicles CSV columns.")
                    return vehicles

                for row in reader:
                    vehicle = Vehicle(
                        vehicle_id=row["vehicle_id"].strip(),
                        registration_no=row["registration_no"].strip(),
                        driver_name=row["driver_name"].strip(),
                        driver_mobile=row["driver_mobile"].strip(),
                        zone_id=row["zone_id"].strip(),
                        speed_limit_kmph=float(row["speed_limit_kmph"]),
                        idle_litres_per_hour=float(row["idle_litres_per_hour"])
                    )

                    vehicles[vehicle.vehicle_id] = vehicle

            print("Total vehicles registered:", len(vehicles))
            return vehicles

        except (FileNotFoundError, OSError, ValueError, KeyError) as error:
            print("ERROR reading vehicles:", error)
            return {}

    def read_zones(self, file_path):
        zones = {}

        try:
            with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                required = [
                    "zone_id", "zone_name", "min_lat",
                    "max_lat", "min_lon", "max_lon"
                ]

                if not reader.fieldnames or not all(
                    column in reader.fieldnames for column in required
                ):
                    print("ERROR: Invalid zones CSV columns.")
                    return zones

                for row in reader:
                    zone = GeofenceZone(
                        zone_id=row["zone_id"].strip(),
                        zone_name=row["zone_name"].strip(),
                        min_latitude=float(row["min_lat"]),
                        max_latitude=float(row["max_lat"]),
                        min_longitude=float(row["min_lon"]),
                        max_longitude=float(row["max_lon"])
                    )

                    zones[zone.zone_id] = zone

            print("Total zones registered:", len(zones))
            return zones

        except (FileNotFoundError, OSError, ValueError, KeyError) as error:
            print("ERROR reading zones:", error)
            return {}

    def read_gps_data(self, file_path):
        gps_records = []
        self.errors = []

        try:
            with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                if not reader.fieldnames:
                    print("ERROR: CSV file is empty or has no header.")
                    return []

                official_format = all(
                    column in reader.fieldnames
                    for column in self.REQUIRED_COLUMNS
                )

                old_format = all(
                    column in reader.fieldnames
                    for column in [
                        "vehicle_id", "timestamp", "latitude",
                        "longitude", "speed", "ignition_status"
                    ]
                )

                if not official_format and not old_format:
                    missing = [
                        column for column in self.REQUIRED_COLUMNS
                        if column not in reader.fieldnames
                    ]
                    print("ERROR: Missing CSV columns:", missing)
                    return []

                for line_no, row in enumerate(reader, start=2):

                    if not row or all(
                        value is None or not str(value).strip()
                        for value in row.values()
                    ):
                        continue

                    vehicle_id = (row.get("vehicle_id") or "").strip()
                    ping_id = ""

                    try:
                        if official_format:
                            ping_id = (row.get("ping_id") or "").strip()
                            speed_value = row.get("speed_kmph")
                            ignition_value = row.get("ignition")
                        else:
                            ping_id = "LEGACY-" + str(line_no)
                            speed_value = row.get("speed")
                            ignition_value = row.get("ignition_status")

                        ping = GPSPing(
                            ping_id=ping_id,
                            vehicle_id=vehicle_id,
                            timestamp=row["timestamp"].strip(),
                            latitude=float(row["latitude"]),
                            longitude=float(row["longitude"]),
                            speed_kmph=float(speed_value),
                            ignition=ignition_value.strip().upper()
                        )

                        if not ping.validate_ping():
                            raise ValueError("Invalid GPS record")

                        ping.line_no = line_no
                        gps_records.append(ping)

                    except (ValueError, KeyError, TypeError, AttributeError) as error:
                        self.errors.append({
                            "line_no": line_no,
                            "ping_id": ping_id,
                            "vehicle_id": vehicle_id,
                            "reason": str(error)
                        })

            print("Total GPS records loaded:", len(gps_records))
            return gps_records

        except FileNotFoundError:
            print("ERROR: GPS data file not found.")
            return []

        except OSError as error:
            print("ERROR: Unable to read CSV file:", error)
            return []