# GPS Tracker Fleet Violation and Idling Cost Engine

**An intelligent Python-based vehicle fleet monitoring and violation detection system using GPS telemetry data.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Project-Completed-success)
![Domain](https://img.shields.io/badge/Domain-IoT%20%7C%20Vehicle%20Telematics-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 1. Project Overview

The **GPS Tracker Fleet Violation and Idling Cost Engine** is a Python-based fleet monitoring system designed to process GPS telemetry data, detect vehicle violations, monitor driver behaviour, and calculate fuel costs associated with vehicle idling.

The system analyzes timestamped GPS records and identifies operational irregularities such as overspeeding, geofence violations, prolonged idling, night driving, and GPS signal loss.

It also calculates idling fuel consumption costs and generates daily driver performance reports, helping fleet operators improve vehicle utilization, monitor driver behaviour, and reduce unnecessary operational expenses.

The application follows a **command-file-driven architecture**, processing vehicle information, geographical zones, and GPS data from structured CSV files.

## 2. Problem Statement

Fleet operators face several challenges in monitoring vehicles efficiently:

- Difficulty tracking vehicle movement across predefined geographical boundaries.
- Overspeeding and unsafe driving behaviour.
- Fuel wastage caused by prolonged vehicle idling.
- Unauthorized or unusual vehicle activity during restricted hours.
- GPS connectivity interruptions and missing location updates.
- Lack of consolidated reports for evaluating driver performance.

This project addresses these challenges through automated GPS data processing, event detection, cost calculation, and daily reporting.

## 3. Key Features

### Vehicle and Fleet Management
- Register multiple vehicles with their respective driver details.
- Maintain vehicle-specific speed limits and idle fuel consumption rates.
- Associate vehicles with predefined geographical zones.

### GPS Data Processing
- Read and process timestamped GPS records from CSV files.
- Validate incoming GPS records.
- Handle invalid records, unknown vehicles, and out-of-order timestamps.

### Automated Violation Detection

The system detects five major event categories:

| Event | Description |
|---|---|
| GEOFENCE | Detects vehicles operating outside their assigned geographical boundaries. |
| OVERSPEED | Identifies vehicles exceeding their configured speed limits. |
| IDLING | Detects prolonged vehicle idling based on ignition and duration conditions. |
| NIGHT_DRIVE | Identifies vehicle movement during configured night hours. |
| GPS_LOST | Detects interruptions in GPS updates beyond the defined threshold. |

The system records event start and end timestamps and calculates event durations where applicable.

### Idling Cost Calculation
- Calculates fuel consumed during idling.
- Uses vehicle-specific idle fuel consumption rates.
- Estimates the associated fuel cost.
- Includes idling cost information in the generated reports.

### Driver Performance Scoring
- Generates daily driver performance scores.
- Evaluates vehicle activity using detected events.
- Produces consolidated fleet performance information.

### Automated Report Generation
The application generates three CSV reports:

| Report | Purpose |
|---|---|
| `event_log.csv` | Contains detected vehicle events and their details. |
| `daily_report.csv` | Provides daily vehicle statistics, idling costs, and driver scores. |
| `errors.csv` | Records invalid or rejected GPS records and processing errors. |

## 4. System Architecture

The project follows a modular architecture, separating GPS data processing, event detection, cost calculation, and report generation.

```text
                 INPUT DATA
                     |
          +----------+----------+
          |          |          |
       Vehicles    Zones     GPS Data
          |          |          |
          +----------+----------+
                     |
                     v
              DATA READER
                     |
                     v
             DATA VALIDATION
                     |
                     v
             EVENT DETECTION
                     |
       +-------------+-------------+
       |             |             |
    GEOFENCE      OVERSPEED      IDLING
       |             |             |
       +-------------+-------------+
                     |
          +----------+----------+
          |                     |
       NIGHT DRIVE           GPS LOST
          |                     |
          +----------+----------+
                     |
                     v
             COST CALCULATION
                     |
                     v
           DRIVER SCORE ENGINE
                     |
                     v
             REPORT GENERATION
                     |
          +----------+----------+
          |          |          |
       Event Log  Daily Report  Errors
          CSV        CSV         CSV
```

## 5. Technology Stack

| Technology | Usage |
|---|---|
| Python 3.10+ | Core programming language |
| CSV | Input data and report storage |
| Python Standard Library | Data processing, timestamps, calculations, and file handling |
| Unittest | Unit testing and validation |
| Git | Version control |
| GitHub | Source code hosting |

## 6. Project Structure

```text
GPS-Tracker-Fleet-Violation-System-E019-ECE-013/
│
├── data/
│   ├── vehicles.csv
│   ├── zones.csv
│   ├── gps_data.csv
│   ├── pings.csv
│   ├── commands.txt
│   └── README.md
│
├── src/
│   ├── __init__.py
│   ├── data_reader.py
│   ├── gps_validator.py
│   ├── event_detector.py
│   ├── geofence.py
│   ├── overspeed.py
│   ├── idling.py
│   ├── night_drive.py
│   ├── gps_lost.py
│   ├── cost_calculator.py
│   ├── driver_score.py
│   ├── report_generator.py
│   └── ...
│
├── tests/
│   ├── test_geofence.py
│   ├── test_overspeed.py
│   ├── test_idling.py
│   ├── test_gps_lost.py
│   ├── test_night_drive.py
│   ├── test_cost_calculator.py
│   └── ...
│
├── PHASE-1-DESIGN/
│   └── ECE-013_GPS_Fleet_Design_Document.docx
│
├── main.py
├── .gitignore
├── event_log.csv
├── daily_report.csv
└── errors.csv
```

*Note: The structure above highlights the major project components. Individual module and test filenames may vary with implementation.*

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or higher.
- Git.
- Visual Studio Code or any Python-supported IDE.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Manasar115/GPS-Tracker-Fleet-Violation-System-E019-ECE-013-.git
```

### Step 2: Navigate to the Project Directory

```bash
cd GPS-Tracker-Fleet-Violation-System-E019-ECE-013-
```

### Step 3: Run the Application

```bash
python main.py
```

The application reads the configured input files, validates GPS records, processes vehicle activity, detects violations, and generates the corresponding reports.

## 8. Running Unit Tests

The project includes unit tests to verify the functionality of individual components.

Run all tests using:

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- Geofence boundary and location detection.
- Overspeed detection and threshold conditions.
- Idling duration and ignition conditions.
- GPS signal loss detection and recovery.
- Night driving detection.
- Idling fuel cost calculations.
- Driver score calculations.
- Fleet report generation.
- GPS record validation.

## 9. Output and Reports

After successful execution, the system generates the following reports:

### Event Log — `event_log.csv`

Stores detected events with information such as:

- Vehicle ID.
- Event type.
- Event start time.
- Event end time.
- Event duration.
- Related event details and calculated costs, where applicable.

### Daily Report — `daily_report.csv`

Provides a daily summary containing:

- Vehicle identification.
- Driver performance score.
- Total idling duration.
- Idling fuel cost.
- Other daily fleet statistics.

### Error Report — `errors.csv`

Maintains records of rejected or invalid GPS data, including:

- Invalid GPS coordinates.
- Unknown vehicle identifiers.
- Out-of-order GPS timestamps.
- Other data validation errors.

## 10. Applications

This project can be applied in:

- Commercial vehicle fleet management.
- Logistics and transportation companies.
- Delivery and distribution services.
- School and employee transportation monitoring.
- Vehicle telematics systems.
- Fuel consumption and operational cost monitoring.

## 11. Future Enhancements

The current implementation uses CSV-based input and output. The following enhancements can extend the system:

- Interactive fleet monitoring dashboard using Streamlit.
- Real-time GPS tracking through IoT devices.
- Integration with cloud databases.
- Map-based visualization of vehicle locations.
- Automated notifications for detected violations.
- Advanced analytics for driver behaviour.
- Predictive maintenance and fuel optimization.

## 12. Learning Outcomes

Through this project, the following technical concepts were implemented:

- Modular Python programming.
- File handling and CSV processing.
- GPS coordinate validation.
- Geographical boundary detection.
- Timestamp and duration calculations.
- Event-driven processing.
- Fuel cost estimation.
- Driver performance evaluation.
- Unit testing and debugging.
- Version control using Git and GitHub.

## 13. Project Information

| Detail | Information |
|---|---|
| Project Code | ECE-013 |
| Project Title | GPS Tracker Fleet Violation and Idling Cost Engine |
| Domain | IoT / Vehicle Telematics |
| Programming Language | Python |
| Application Type | Command-Line / CSV-Driven System |
| Testing Framework | Python Unittest |
| Repository | [GitHub Repository](https://github.com/Manasar115/GPS-Tracker-Fleet-Violation-System-E019-ECE-013-) |

---

**Developed as an ECE-013 project focused on intelligent fleet monitoring, automated violation detection, and vehicle operational cost analysis.**
