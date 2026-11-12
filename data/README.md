# ECE-013 – GPS Tracker Fleet Violation and Idling Cost Engine — Sample Data Pack
Prepared by 10 SECONDS for Team E019.

This pack is the input for a fleet telematics engine: 12 delivery vans in 3 rectangular Bengaluru zones, GPS pings every minute for 2026-10-15. Your engine reads `commands.txt`, loads the masters and pings, detects GEOFENCE / OVERSPEED / IDLING / NIGHT_DRIVE / GPS_LOST events, and prints the event log and the daily fleet report.

Pack conventions where the brief is silent: process each vehicle's pings in timestamp order (the file is sorted by timestamp then vehicle_id, except for one planted out-of-order row); a ping whose timestamp is not later than that vehicle's last accepted ping is out of order and rejected. A ping on the rectangle edge (latitude equal to min_lat/max_lat or longitude equal to min_lon/max_lon) is INSIDE. Overspeed means speed > 1.10 × limit (compare `speed*10 > limit*11` to avoid floating-point surprises). Each ping stands for one minute; an idle ping is ignition ON with speed 0.0. The night window is 23:00:00 ≤ time < 05:00:00. A gap is the difference between two consecutive accepted pings of the same vehicle; more than 15:00 minutes is GPS_LOST.

Event times: `start_time` is the timestamp of the ping at which the event opens (2nd outside ping, 3rd over-limit ping, 11th idle ping, first moving night ping; for GPS_LOST the last ping before the gap); `end_time` is the closing ping (first inside ping; first ping at or below the limit; first ping that is not idle; 5th consecutive ping at or below 5 km/h; for GPS_LOST the first ping after the gap). Idle minutes for the cost = end_time − start_time of the IDLING event in minutes.

## Files
| File | What it holds | Rows |
|---|---|---|
| zones.csv | Rectangular geofence zones | 3 |
| vehicles.csv | Vans with driver, zone, speed limit and idle fuel burn | 12 |
| pings.csv | 1-minute GPS pings for 2026-10-15 | 2541 |
| commands.txt | Load commands, then the two print commands | 5 |

Volumes in this sample are reduced for email delivery; the hidden evaluation set is larger and uses the same schema. (Here each van's tracker covers roughly a 3.5-hour shift; the evaluation set covers full 14-hour shifts, about 10,000 pings.)

## Column reference
Conventions: dates `YYYY-MM-DD`; timestamps `YYYY-MM-DD HH:MM:SS` (24h, IST, no timezone suffix); money in Rs as plain decimals (no commas, no symbol); percentages as plain numbers (12.5 = 12.5%); booleans `true`/`false`; IDs uppercase with a fixed prefix.

### zones.csv
| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| zone_id | string | ZONE-x | ZONE-S, ZONE-E, ZONE-N | Primary key |
| zone_name | string | - | free text |  |
| min_lat | decimal | degrees, 5 dp | -90 to 90 | Rectangle edge (inclusive) |
| max_lat | decimal | degrees, 5 dp | -90 to 90 | Rectangle edge (inclusive) |
| min_lon | decimal | degrees, 5 dp | -180 to 180 | Rectangle edge (inclusive) |
| max_lon | decimal | degrees, 5 dp | -180 to 180 | Rectangle edge (inclusive) |

### vehicles.csv
| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| vehicle_id | string | VEH-nn | VEH-01 … VEH-12 | Primary key |
| registration_no | string | KA-nn-XX-nnnn |  | Not used by any rule |
| driver_name | string | - |  | One driver per vehicle for the day |
| driver_mobile | string | 10 digits | starts 6–9 | Not used by any rule |
| zone_id | string | ZONE-x | must exist in zones.csv | The vehicle's assigned geofence |
| speed_limit_kmph | integer | km/h | 40, 50, 60 |  |
| idle_litres_per_hour | decimal | litres/hour, 1 dp | 0.8–1.4 | Fuel price is Rs 92 per litre (from the brief) |

### pings.csv
| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| ping_id | string | PNG-nnnnn | unique | Numbered in file order |
| vehicle_id | string | VEH-nn | should exist in vehicles.csv | One planted unregistered tracker (VEH-13) |
| timestamp | timestamp | YYYY-MM-DD HH:MM:SS | 2026-10-15 | One row per vehicle per minute while the tracker is on; two planted gaps; one out-of-order row |
| latitude | decimal | degrees, 5 dp | -90 to 90 | Values outside the range are rejected |
| longitude | decimal | degrees, 5 dp | -180 to 180 | Values outside the range are rejected |
| speed_kmph | decimal | km/h, 1 dp | 0.0 and above |  |
| ignition | string | - | ON, OFF | Idle = ON with speed 0.0; OFF with speed 0.0 is parked, not idling |

## Command file format
`commands.txt` holds one command per line as `COMMAND_NAME|arg1|arg2|...`. Commands must be processed in file order, top to bottom. Lines starting with `#` are comments and blank lines are ignored.

| Command | Arguments (in order) | Meaning |
|---|---|---|
| LOAD_ZONES | file | Load zones.csv |
| LOAD_VEHICLES | file | Load vehicles.csv |
| LOAD_PINGS | file | Load pings.csv, validate each ping, run the event detectors |
| EVENT_LOG | vehicle_id or ALL | Print the event log (all vehicles, ordered by vehicle_id then start_time) |
| DAILY_REPORT | YYYY-MM-DD | Print the daily fleet report for that date |

`event_type` is one of GEOFENCE, OVERSPEED, IDLING, NIGHT_DRIVE, GPS_LOST. `idle_cost_rs` is 0.00 for every event that is not IDLING. `duration_min` is end_time − start_time in whole minutes.

## Planted scenarios
Line numbers count the header row as line 1, so the first data row of a CSV is line 2. For commands.txt the line number is the physical line in the file (comment lines included).

- **Ping exactly on the geofence boundary (inside)** — VEH-04 (ZONE-S lat 12.88000–12.95000, lon 77.54000–77.63000): pings.csv line 956 (PNG-00955, VEH-04, 09:19:00) is outside, pings.csv line 966 (PNG-00965, VEH-04, 09:20:00) lies exactly on the zone edge (counts as inside, resets the counter), pings.csv line 976 (PNG-00975, VEH-04, 09:21:00) is outside again, pings.csv line 986 (PNG-00985, VEH-04, 09:22:00) back inside — no GEOFENCE event. Compare the real excursion on VEH-11: 7 outside pings from pings.csv line 2381 (PNG-02380, VEH-11, 20:53:00); the event opens at pings.csv line 2382 (PNG-02381, VEH-11, 20:54:00) and closes at pings.csv line 2388 (PNG-02387, VEH-11, 21:00:00).
- **Speed exactly 10% above the limit (not overspeed)** — VEH-09 (limit 50 km/h): 4 consecutive pings at exactly 55.0 km/h starting pings.csv line 1459 (PNG-01458, VEH-09, 10:10:00) — that is exactly 10% above the limit, not more, so no OVERSPEED. Compare VEH-04: OVERSPEED opens at pings.csv line 1910 (PNG-01909, VEH-04, 11:02:00) (3rd over-limit ping); pings.csv line 1918 (PNG-01917, VEH-04, 11:03:00) is above the limit but within 10% so the event stays open; it closes at pings.csv line 1926 (PNG-01925, VEH-04, 11:04:00) (at or below the limit).
- **Idle for exactly 10 minutes then moving** — VEH-01: ignition ON, speed 0.0 for exactly 10 pings from pings.csv line 641 (PNG-00640, VEH-01, 08:46:00), then moving at pings.csv line 726 (PNG-00725, VEH-01, 08:56:00) — no IDLING. Compare VEH-05: 24 idle pings from pings.csv line 1546 (PNG-01545, VEH-05, 10:19:00); IDLING opens at pings.csv line 1641 (PNG-01640, VEH-05, 10:29:00) (11th idle minute) and closes at pings.csv line 1759 (PNG-01758, VEH-05, 10:43:00) = 14 idle minutes.
- **Movement starting at 22:59 and continuing past 23:00** — VEH-11: stationary until 22:58, moving from pings.csv line 2507 (PNG-02506, VEH-11, 22:59:00) (22:59 is outside the night window), NIGHT_DRIVE opens at pings.csv line 2508 (PNG-02507, VEH-11, 23:00:00); speeds 4.0, 5.0, 0.0, 0.0, 0.0 from 23:20 close it at pings.csv line 2532 (PNG-02531, VEH-11, 23:24:00) (5th consecutive ping at or below 5 km/h — 5.0 counts).
- **Gap of exactly 15 minutes (not GPS_LOST)** — VEH-04: pings.csv line 1126 (PNG-01125, VEH-04, 09:36:00) then the next ping pings.csv line 1265 (PNG-01264, VEH-04, 09:51:00) — exactly 15 min apart, so no GPS_LOST and counters are NOT reset. The real gap: VEH-02 pings.csv line 2030 (PNG-02029, VEH-02, 11:18:00) → pings.csv line 2161 (PNG-02160, VEH-02, 11:40:00) is 22 min → GPS_LOST.

Extra traps (realistic things your validation should catch):

- **GPS gap resets the overspeed counter** — VEH-02 has 2 over-limit pings before the 22-min gap (ending pings.csv line 2030 (PNG-02029, VEH-02, 11:18:00)) and 2 after it (from pings.csv line 2161 (PNG-02160, VEH-02, 11:40:00)); because GPS_LOST resets counters, there is NO OVERSPEED here (4 over-limit pings in total, never 3 consecutive after a reset).
- **Out-of-order ping inside an overspeed run** — pings.csv line 152 (PNG-00151, VEH-08, 07:04:00) carries a timestamp 5 min earlier than the VEH-08 ping just before it (pings.csv line 151 (PNG-00150, VEH-08, 07:09:00)); reject it with an error line. It shows speed 0.0 — if you let it reset the counter you will miss the OVERSPEED that opens at pings.csv line 155 (PNG-00154, VEH-08, 07:10:00).
- **Invalid coordinates** — pings.csv line 953 (PNG-00952, VEH-01, 09:19:00) latitude 91.24418 and pings.csv line 1243 (PNG-01242, VEH-12, 09:48:00) longitude 277.59213 are outside the valid ranges (-90..90, -180..180) → reject, error line, counters untouched.
- **Ping from an unregistered tracker** — pings.csv line 1178 (PNG-01177, VEH-13, 09:41:00) to pings.csv line 1198 (PNG-01197, VEH-13, 09:43:00) are from VEH-13, which is not in vehicles.csv → reject each with an error line.
- **Movement starting exactly at 05:00:00** — VEH-08 is parked from 04:50 and starts moving at pings.csv line 12 (PNG-00011, VEH-08, 05:00:00); the night window ends at 05:00:00 (exclusive), so no NIGHT_DRIVE.
- **Driver score floor** — VEH-03 has 11 separate OVERSPEED bursts (first opens at pings.csv line 250 (PNG-00249, VEH-03, 07:37:00)); 100 - 110 = -10 → score floors at 0.

## What is NOT in this pack
Expected outputs are not provided for this set. Validate your engine with your own test suite against the rules in your brief (BR-01 … BR-07). A separate hidden input set with the same schema will be used at final evaluation; outputs are compared field-for-field, so follow the column formats above exactly in your own output.

## Output format expected at evaluation
Produce these files (CSV, header row, same conventions as above). Column order matters.

### event_log.csv
One row per detected event, ordered by vehicle_id then start_time.

Columns in order: `vehicle_id`, `event_type`, `start_time`, `end_time`, `duration_min`, `idle_cost_rs`

### daily_report.csv
One row per registered vehicle for the date, ordered by vehicle_id. `idle_cost_rs` = sum over IDLING events of idle minutes / 60 × idle_litres_per_hour × 92, rounded to 2 decimals per event.

Columns in order: `date`, `vehicle_id`, `driver_name`, `geofence_events`, `overspeed_events`, `idling_events`, `night_drive_events`, `gps_lost_events`, `idle_minutes`, `idle_cost_rs`, `driver_score`

### errors.csv
One row per rejected ping, in file order.

Columns in order: `line_no`, `ping_id`, `vehicle_id`, `reason`
