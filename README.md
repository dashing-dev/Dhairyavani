IoT-Based Sensor Monitoring System
Overview

This project demonstrates a smart monitoring system using an ESP32 microcontroller, Django web server, and machine learning models for real-time disaster preparedness. The system reads data from vibration and water level sensors, sends it to a Django server using APIs, and provides risk assessment based on predefined thresholds and ML models.
Features

    Sensor Integration: Real-time data collection from vibration and water level sensors.
    API Communication: Data transmission from ESP32 to Django server using REST API.
    ML-Based Risk Analysis: Predictive analysis using machine learning models for three-factor hazard detection.
    User Interaction:
        Normal users can view live sensor data, receive alerts, and mark themselves safe in emergencies.
        Admins can trigger notifications and send custom alerts via email.
    Alert System: Automated notifications sent when thresholds are breached.

System Architecture

    ESP32:
        Reads analog data from sensors.
        Connects to Wi-Fi to send data to the Django server.

    Django Server:
        Receives and stores sensor data through API endpoints.
        Processes data using ML models for risk prediction.
        Sends email alerts to users in critical conditions.

    Frontend:
        Provides users with a graphical view of live and historical sensor data.
        Enables admins to manage alerts and notifications.

Getting Started
Prerequisites

    Hardware:
        ESP32 microcontroller.
        Vibration sensor (connected to GPIO36).
        Water level sensor (connected to GPIO39).
    Software:
        Python 3.9 or higher.
        Django 5.1.3.
        ESP32 Arduino Core.

ESP32 Configuration

    Connect:
        Vibration Sensor (Ao) → GPIO36 (VP pin).
        Water Level Sensor (S) → GPIO39 (VN pin).

    Install Arduino IDE and ESP32 board support:
        Follow this guide to set up ESP32 in Arduino IDE.

    Upload the ESP32 code:
        Replace ssid, password, and serverURL in the code with your network credentials and Django server URL.
        Upload the code to the ESP32.

Django Server Setup

    Clone the repository:

git clone https://github.com/Dhairyavani/sensormonitoring.git
cd sensormonitoring

Install dependencies:

pip install -r requirements.txt

Configure settings:

    Add your local IP address in ALLOWED_HOSTS in settings.py.

Start the server:

    python manage.py runserver 0.0.0.0:8000

API Endpoint

    URL: /api/sensor-data/
    Method: POST
    Payload:

    {
      "vibration": <int>,
      "water_level": <int>
    }

Screenshots

Insert snapshots of the dashboard, alerts, and ML-based prediction results here.
Future Enhancements

    Add support for more sensors like temperature and humidity.
    Incorporate advanced ML models for better hazard prediction.
    Enable real-time push notifications for mobile devices.

Contributors

    Your Name
    Developer & IoT Enthusiast
    LinkedIn

Feel free to fork and contribute!
