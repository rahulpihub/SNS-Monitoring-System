Here's the complete README content for you to copy and paste:

---

# Ihub Monitoring System

> A Flask-based system for monitoring employee work hours and attendance using YOLO object detection. The system provides real-time logging, attendance tracking, and summary generation for employee activities.

---

## Introduction

The Ihub Monitoring System is designed to track employee work hours and attendance using video streams. It leverages the YOLO object detection model to identify employees and log their activities, such as login and logout times. The system generates detailed CSV reports summarizing work hours and attendance logs.

---

## Features

- **Real-Time Work Monitoring**: Stream video feeds and log employee activities.
- **Attendance Tracking**: Monitor employee login/logout times and generate detailed logs.
- **Automatic Summary Reports**: Generate daily summaries of work hours in CSV format.
- **Interactive Web Interface**: Simple UI for toggling work monitoring and attendance tracking.
- **YOLO Object Detection**: Use advanced object detection for employee identification.

---

## Technologies Used

- **Backend**: Flask
- **Object Detection**: YOLO
- **Frontend**: HTML, CSS, JavaScript
- **Data Handling**: Pandas
- **Database/Storage**: CSV files

---

## Setup and Installation

### Prerequisites

1. Python 3.x installed on your machine.
2. YOLO model weights (`best.pt`) downloaded and placed in the appropriate path.
3. OpenCV library installed.

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ihub-monitoring-system.git
   cd ihub-monitoring-system/flask
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the following directories exist:
   - `monitoringdata/` for storing monitoring logs.
   - `monitoringsummary/` for storing summary reports.

4. Place the YOLO model weights (`best.pt`) in the specified path (`R:\\ihub\\Work\\Nov\\Monitoring Project\\flask\\best.pt`).

---

## Usage

### Starting the Application

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

### Monitoring Work Hours

- Click the **Start Work Hours Monitoring** button to begin monitoring.
- Real-time video stream will appear, and activities will be logged.
- Click **Stop Work Hours Monitoring** to end the session and save a summary.

### Attendance Tracking

- Navigate to the **Attendance Monitoring** page.
- Monitor employees' login and logout times.
- Detailed logs are displayed for each action.

---

## Folder Structure

```plaintext
flask/
├── app.py                 # Main Flask application
├── templates/             # HTML templates for the web interface
│   ├── index.html         # Main dashboard
│   ├── attendance.html    # Attendance tracking page
├── static/                # Static files (CSS, JavaScript)
│   ├── style.css          # CSS styles for the UI
│   ├── attendance.js      # JS for attendance monitoring
│   ├── video_feed.js      # JS for work hours monitoring
├── monitoringdata/        # Folder for logging real-time data
├── monitoringsummary/     # Folder for storing summary CSVs
└── best.pt                # YOLO model weights (add this file manually)
```

