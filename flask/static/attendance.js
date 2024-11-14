function startAttendance() {
    fetch('/video_feed_attendance')
        .then(response => response.text())
        .then(data => {
            document.getElementById("attendanceMessage").innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
