from flask import Flask, render_template, Response, jsonify
import os
import cv2
import pandas as pd
from ultralytics import YOLO
from datetime import datetime

app = Flask(__name__)

# Paths
monitoring_data_dir = 'monitoringdata'
summary_dir = 'R:\\ihub\\Work\\Nov\\Monitoring Project\\flask\\monitoringsummary'
summary_file = os.path.join(summary_dir, 'monitoring_summary.csv')

# Ensure summary directory exists and create summary file with headers if it doesn't exist
os.makedirs(summary_dir, exist_ok=True)
if not os.path.exists(summary_file):
    pd.DataFrame(columns=['Employee Name', 'Date', 'Login Time', 'Logout Time', 'Total Working Hours']).to_csv(summary_file, index=False)

# Set up a folder for monitoring data and generate a unique filename
def get_monitoring_csv_filename(base_dir=monitoring_data_dir):
    os.makedirs(base_dir, exist_ok=True)  # Ensure the folder exists
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(base_dir, f'monitoring_data_{timestamp}.csv')
    pd.DataFrame(columns=['Employee Name', 'Date', 'Timestamp']).to_csv(csv_path, index=False)
    return csv_path

# Initialize a global variable for the monitoring CSV file
monitoring_csv_file = None

# Load YOLO model
def load_model(model_path='R:\\ihub\\Work\\Nov\\Monitoring Project\\flask\\best.pt'):
    model = YOLO(model_path)  # Load the YOLO model once at startup
    return model

model = load_model()  # Initialize the model

# Global variable to control monitoring status
is_monitoring = False

# Function to log work hours in the monitoring CSV
def log_detection(employee_name):
    now = datetime.now()
    date_today = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")
    
    new_entry = pd.DataFrame({
        'Employee Name': [employee_name],
        'Date': [date_today],
        'Timestamp': [time_now]
    })
    new_entry.to_csv(monitoring_csv_file, mode='a', header=False, index=False)
    return time_now

# Function to calculate total monitoring time and save to summary CSV
def calculate_total_time(csv_file):
    df = pd.read_csv(csv_file)
    if not df.empty:
        first_log = df.iloc[0]
        last_log = df.iloc[-1]
        employee_name = first_log['Employee Name']
        date = first_log['Date']
        login_time = first_log['Timestamp']
        logout_time = last_log['Timestamp']

        # Convert timestamps to datetime objects to calculate the time difference
        start_time = datetime.strptime(login_time, "%H:%M:%S")
        end_time = datetime.strptime(logout_time, "%H:%M:%S")
        total_time = end_time - start_time

        # Append the monitoring summary to the summary CSV file
        summary_entry = pd.DataFrame({
            'Employee Name': [employee_name],
            'Date': [date],
            'Login Time': [login_time],
            'Logout Time': [logout_time],
            'Total Working Hours': [str(total_time)]
        })
        summary_entry.to_csv(summary_file, mode='a', header=False, index=False)
        print(f"Monitoring summary saved to {summary_file}")

# Video streaming generator function for main video feed with detection logging
def generate_main_frames():
    cap = cv2.VideoCapture(0)

    while cap.isOpened() and is_monitoring:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        
        if hasattr(results[0], 'boxes'):
            for box in results[0].boxes:
                class_name = model.names[int(box.cls[0].item())]
                
                log_time = log_detection(class_name)
                print(f"{class_name} detected and logged at {log_time}")

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Video streaming generator function for attendance monitoring
def generate_attendance_frames():
    cap = cv2.VideoCapture(0)
    last_detected_name = None
    last_detected_time = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        frame_class_names = []

        if hasattr(results[0], 'boxes'):
            for box in results[0].boxes:
                class_name = model.names[int(box.cls[0].item())]
                frame_class_names.append(class_name)

                current_time = datetime.now()
                if class_name != last_detected_name or (current_time - last_detected_time).total_seconds() > 5:
                    login_time = log_detection(class_name)
                    last_detected_name = class_name
                    last_detected_time = current_time
                    yield f"<div>{class_name} has logged in at {login_time}. Please allow the next person.</div>".encode()

                else:
                    logout_time = log_detection(class_name)
                    last_detected_name = class_name
                    last_detected_time = current_time
                    yield f"<div>{class_name} has logged out at {logout_time}. Please allow the next person.</div>".encode()

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Start monitoring
@app.route('/start_monitoring')
def start_monitoring():
    global is_monitoring, monitoring_csv_file
    is_monitoring = True
    monitoring_csv_file = get_monitoring_csv_filename()
    return jsonify({"message": "Work Hours Monitoring started. Logging to: " + monitoring_csv_file})

# Stop monitoring and calculate total time
@app.route('/stop_monitoring')
def stop_monitoring():
    global is_monitoring
    is_monitoring = False
    calculate_total_time(monitoring_csv_file)  # Calculate total time when stopping
    return jsonify({"message": "Work Hours Monitoring stopped. Report saved to: " + monitoring_csv_file})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_main_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_attendance')
def video_feed_attendance():
    return Response(generate_attendance_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
