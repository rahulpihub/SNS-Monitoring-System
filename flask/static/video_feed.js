let monitoringActive = false;

function toggleMonitoring() {
    const videoFeed = document.getElementById("videoFeed");
    const toggleButton = document.getElementById("toggleButton");

    if (!monitoringActive) {
        // Start the monitoring feed
        startDetection().then(() => {
            videoFeed.src = videoFeedUrl;
            videoFeed.style.display = "block";
            toggleButton.textContent = "Stop Work Hours Monitoring";
            monitoringActive = true;
        });
    } else {
        // Stop the monitoring feed
        stopDetection().then(() => {
            videoFeed.src = "";
            videoFeed.style.display = "none";
            toggleButton.textContent = "Start Work Hours Monitoring";
            monitoringActive = false;
        });
    }
}

function startDetection() {
    return fetch('/start_monitoring')
        .then(response => response.json())
        .then(data => {
            document.getElementById("message").textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function stopDetection() {
    return fetch('/stop_monitoring')
        .then(response => response.json())
        .then(data => {
            document.getElementById("message").textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
