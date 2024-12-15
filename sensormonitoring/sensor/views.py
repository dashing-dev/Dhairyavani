# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required
# from .models import SensorReading, Notification
# from .forms import UserRegistrationForm, SensorInputForm
# from django.contrib.auth.models import User

# # User registration
# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('dashboard')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'sensor/register.html', {'form': form})

# # User login
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             return render(request, 'sensor/login.html', {'error': 'Invalid username or password'})
#     return render(request, 'sensor/login.html')

# # User logout
# def user_logout(request):
#     logout(request)
#     return redirect('login')

# # Sensor data input (for admin or manual testing)
# @login_required
# def sensor_input(request):
#     if request.method == 'POST':
#         form = SensorInputForm(request.POST)
#         if form.is_valid():
#             sensor_data = form.save(commit=False)
#             sensor_data.user = request.user  # Assign the logged-in user
#             sensor_data.save()
#             return redirect('dashboard')
#     else:
#         form = SensorInputForm()
#     return render(request, 'sensor/sensor_input.html', {'form': form})

# # View sent notifications history
# @login_required
# def notification_history(request):
#     notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
#     return render(request, 'sensor/notification_history.html', {'notifications': notifications})



# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import SensorReading

# @csrf_exempt
# def sensor_data_input(request):
#     if request.method == 'POST':
#         try:
#             # Parse the JSON data from the request
#             data = json.loads(request.body)
#             water_level = data.get('water_level')
#             vibration = data.get('vibration')

#             # Save the data to the database
#             SensorReading.objects.create(water_level=water_level, vibration=vibration)

#             return JsonResponse({'message': 'Data saved successfully'}, status=201)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
    

# from django.shortcuts import render

# def landing_page(request):
#     return render(request, 'sensor/landing_page.html')

# def home(request):
#     return render(request,'sensor/home.html')


# from django.utils.timezone import now
# from django.contrib.auth.decorators import login_required
# from .models import SensorReading
# import datetime

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from datetime import date  # Import only what's needed
# from .models import SensorReading  # Ensure your model is correctly imported

# @login_required
# def dashboard(request):
#     # Get today's date
#     today = date.today()

#     # Filter sensor readings for the current day
#     sensor_data = SensorReading.objects.filter(
#         timestamp__date=today
#     ).order_by('timestamp')

#     # Ensure there is data to process
#     if sensor_data.exists():
#         # Prepare data for the graph
#         timestamps = [reading.timestamp.strftime("%H:%M") for reading in sensor_data]
#         water_levels = [reading.water_level for reading in sensor_data]
#         vibrations = [reading.vibration for reading in sensor_data]
#     else:
#         # Default empty values if no data exists
#         timestamps = []
#         water_levels = []
#         vibrations = []

#     # Pass data to the template
#     context = {
#         'timestamps': timestamps,
#         'water_levels': water_levels,
#         'vibrations': vibrations,
#     }
#     return render(request, 'sensor/dashboard.html', context)


# from .utils import send_notification_email
# from .models import SensorReading
# from django.conf import settings
# import requests

# def process_sensor_data(vibration, water_level):
#     # Define thresholds
#     vibration_threshold = 1.0
#     water_level_threshold = 2.0

#     # Check for alerts
#     alert_message = ""
#     if vibration > vibration_threshold:
#         alert_message += "High vibration levels detected.\n"
#     if water_level > water_level_threshold:
#         alert_message += "High water levels detected.\n"

#     # Compare with external APIs (e.g., OpenWeather and USGS)
#     # Dummy example to simulate validation
#     weather_api = "http://api.openweathermap.org/data/2.5/weather?q=your_city&appid=your_api_key"
#     usgs_api = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"

#     try:
#         weather_response = requests.get(weather_api).json()
#         usgs_response = requests.get(usgs_api).json()

#         if "rain" in weather_response:
#             alert_message += "Rain detected, increasing flood risk.\n"
#         if usgs_response.get("metadata", {}).get("count", 0) > 0:
#             alert_message += "Seismic activity detected, increasing landslide risk.\n"
#     except Exception as e:
#         print(f"Error fetching external API data: {e}")

#     # Save the sensor reading
#     reading = SensorReading.objects.create(vibration=vibration, water_level=water_level)

#     # Send alert email if there's a message
#     if alert_message:
#         subject = "Sensor Alert Notification"
#         message = f"{alert_message}\nTimestamp: {reading.timestamp}\n"
#         recipient_list = [user.email for user in User.objects.filter(is_staff=False)]  # Non-admin users
#         send_notification_email(subject, message, recipient_list)

# from django.contrib.auth.decorators import user_passes_test
# from django.shortcuts import render, redirect
# from .forms import AdminNotificationForm
# from .utils import send_notification_email

# @user_passes_test(lambda u: u.is_staff)  # Ensure only admins can access
# def admin_notification(request):
#     if request.method == "POST":
#         form = AdminNotificationForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             recipient_email = form.cleaned_data['recipient_email']
#             send_notification_email(subject, message, [recipient_email])
#             return redirect('dashboard')  # Redirect to dashboard after sending
#     else:
#         form = AdminNotificationForm()
#     return render(request, 'sensor/admin_notification.html', {'form': form})



# # views.py

# from django.shortcuts import render
# from .models import Notification

# def notification_history(request):
#     # Fetch notifications for the logged-in user
#     notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
#     return render(request, 'sensor/notification_history.html', {'notifications': notifications})



# from django.contrib.auth.models import User  # Import the User model
# from .utils import send_notification_email
# from .models import SensorReading
# import requests
# from datetime import datetime

# def process_sensor_data(vibration, water_level):
#     # Define thresholds
#     vibration_threshold = 1.0
#     water_level_threshold = 2.0

#     # Check for alerts
#     alert_message = ""
#     if vibration > vibration_threshold:
#         alert_message += "High vibration levels detected.\n"
#     if water_level > water_level_threshold:
#         alert_message += "High water levels detected.\n"

#     # Compare with external APIs (e.g., OpenWeather and USGS)
#     weather_api = "http://api.openweathermap.org/data/2.5/weather?q=your_city&appid=your_api_key"
#     usgs_api = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"

#     try:
#         weather_response = requests.get(weather_api).json()
#         usgs_response = requests.get(usgs_api).json()

#         if "rain" in weather_response:
#             alert_message += "Rain detected, increasing flood risk.\n"
#         if usgs_response.get("metadata", {}).get("count", 0) > 0:
#             alert_message += "Seismic activity detected, increasing landslide risk.\n"
#     except Exception as e:
#         print(f"Error fetching external API data: {e}")

#     # Save the sensor reading
#     reading = SensorReading.objects.create(
#         timestamp=datetime.now(),
#         vibration=vibration,
#         water_level=water_level
#     )

#     # Send alert email if there's a message
#     if alert_message:
#         subject = "Sensor Alert Notification"
#         message = f"{alert_message}\nTimestamp: {reading.timestamp}\n"
#         recipient_list = [user.email for user in User.objects.filter(is_staff=False)]  # Non-admin users
#         send_notification_email(subject, message, recipient_list)

# sensor/views.py
# ------------------------------second version from here ------------------------
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import SensorReading, Notification
# from .forms import UserRegistrationForm, AdminMailForm
# from .utils import send_notification_email
# from datetime import datetime, date
# import requests
# import json

# # ------------------ User Authentication Views ------------------

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Optionally, you can log the user in immediately after registration
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'sensor/register.html', {'form': form})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             return render(request, 'sensor/login.html', {'error': 'Invalid username or password'})
#     return render(request, 'sensor/login.html')


# def user_logout(request):
#     logout(request)
#     return redirect('login')

# # ------------------ Sensor Data Handling ------------------

# @csrf_exempt
# def receive_sensor_data(request):
#     """
#     API endpoint to receive sensor data from ESP8266.
#     Expects JSON data with 'water_level' and 'vibration'.
#     """
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             water_level = data.get('water_level')
#             vibration = data.get('vibration')

#             if water_level is None or vibration is None:
#                 return JsonResponse({'error': 'Missing data fields'}, status=400)

#             # Save the data to the database (user=None for ESP data)
#             SensorReading.objects.create(
#                 water_level=water_level,
#                 vibration=vibration
#             )

#             # Process the data for alerts
#             process_sensor_data(vibration, water_level)

#             return JsonResponse({'message': 'Data received successfully and processed.'}, status=201)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)


# @login_required
# def dashboard(request):
#     """
#     Dashboard view that displays sensor data in graphical format.
#     """
#     today = date.today()
#     sensor_data = SensorReading.objects.filter(timestamp__date=today).order_by('timestamp')

#     if sensor_data.exists():
#         timestamps = [reading.timestamp.strftime("%H:%M") for reading in sensor_data]
#         water_levels = [reading.water_level for reading in sensor_data]
#         vibrations = [reading.vibration for reading in sensor_data]
#     else:
#         timestamps = []
#         water_levels = []
#         vibrations = []

#     context = {
#         'timestamps': timestamps,
#         'water_levels': water_levels,
#         'vibrations': vibrations,
#     }
#     return render(request, 'sensor/dashboard.html', context)


# @login_required
# def notification_history(request):
#     """
#     View to display the logged-in user's notification history.
#     """
#     notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
#     return render(request, 'sensor/notification_history.html', {'notifications': notifications})


# @user_passes_test(lambda u: u.is_staff)
# def send_custom_mail(request):
#     """
#     Admin view to send custom emails to users.
#     """
#     if request.method == 'POST':
#         form = AdminMailForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             recipients = User.objects.filter(is_staff=False).values_list('email', flat=True)

#             # Send email to all non-admin users
#             send_notification_email(subject, message, list(recipients))

#             # Optionally, log this notification in the Notification model for each user
#             for user in User.objects.filter(is_staff=False):
#                 Notification.objects.create(
#                     recipient=user,
#                     subject=subject,
#                     message=message
#                 )

#             return JsonResponse({'status': 'Emails sent successfully!'})
#     else:
#         form = AdminMailForm()
#     return render(request, 'sensor/send_custom_mail.html', {'form': form})

# # ------------------ Helper Function ------------------

# def process_sensor_data(vibration, water_level):
#     """
#     Process sensor data to check for thresholds and validate with external APIs.
#     Sends email notifications if necessary.
#     """
#     # Define thresholds
#     VIBRATION_THRESHOLD = 1.0
#     WATER_LEVEL_THRESHOLD = 2.0

#     alert_message = ""
#     if vibration > VIBRATION_THRESHOLD:
#         alert_message += "High vibration levels detected.\n"
#     if water_level > WATER_LEVEL_THRESHOLD:
#         alert_message += "High water levels detected.\n"

#     # Validate spikes with external APIs
#     # Replace 'your_city' and 'your_api_key' with actual values
#     WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather?q=your_city&appid=your_api_key"
#     USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"

#     try:
#         weather_response = requests.get(WEATHER_API_URL)
#         weather_data = weather_response.json()

#         usgs_response = requests.get(USGS_API_URL)
#         usgs_data = usgs_response.json()

#         # Example logic: Check if it's raining or if there's recent seismic activity
#         if weather_data.get("weather") and any("rain" in condition.get("main", "").lower() for condition in weather_data["weather"]):
#             alert_message += "Rain detected, increasing flood risk.\n"

#         # Check if there have been recent earthquakes (you can refine this as needed)
#         if usgs_data.get("features"):
#             alert_message += "Recent seismic activity detected, increasing landslide risk.\n"

#     except Exception as e:
#         print(f"Error fetching external API data: {e}")

#     # Save the sensor reading
#     SensorReading.objects.create(
#         water_level=water_level,
#         vibration=vibration
#     )

#     # Send alert email if necessary
#     if alert_message:
#         subject = "Sensor Alert Notification"
#         message = f"{alert_message}\nTimestamp: {datetime.now()}\n"
#         recipients = User.objects.filter(is_staff=False).values_list('email', flat=True)
#         send_notification_email(subject, message, list(recipients))

#         # Log notifications in the Notification model
#         for user in User.objects.filter(is_staff=False):
#             Notification.objects.create(
#                 recipient=user,
#                 subject=subject,
#                 message=message
#             )




from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorReading, Notification
from .forms import UserRegistrationForm, AdminMailForm
from .utils import send_simple_message  # Updated to use Mailgun integration
from datetime import datetime, date
import requests
import json

# ------------------ User Authentication Views ------------------

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally, you can log the user in immediately after registration
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'sensor/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'sensor/login.html', {'error': 'Invalid username or password'})
    return render(request, 'sensor/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

# ------------------ Sensor Data Handling ------------------

@csrf_exempt
def receive_sensor_data(request):
    """
    API endpoint to receive sensor data from ESP8266.
    Expects JSON data with 'water_level' and 'vibration'.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            water_level = data.get('water_level')
            vibration = data.get('vibration')

            if water_level is None or vibration is None:
                return JsonResponse({'error': 'Missing data fields'}, status=400)

            # Save the data to the database (user=None for ESP data)
            SensorReading.objects.create(
                water_level=water_level,
                vibration=vibration
            )

            # Process the data for alerts
            process_sensor_data(vibration, water_level)

            return JsonResponse({'message': 'Data received successfully and processed.'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# @login_required
# def dashboard(request):
#     """
#     Dashboard view that displays sensor data in graphical format.
#     """
#     today = date.today()
#     sensor_data = SensorReading.objects.filter(timestamp__date=today).order_by('timestamp')

#     if sensor_data.exists():
#         timestamps = [reading.timestamp.strftime("%H:%M") for reading in sensor_data]
#         water_levels = [reading.water_level for reading in sensor_data]
#         vibrations = [reading.vibration for reading in sensor_data]
#     else:
#         timestamps = []
#         water_levels = []
#         vibrations = []

#     context = {
#         'timestamps': timestamps,
#         'water_levels': water_levels,
#         'vibrations': vibrations,
#     }
#     return render(request, 'sensor/dashboard.html', context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import SensorReading

# @login_required
# def dashboard(request):
#     """
#     Dashboard view that displays sensor data in graphical format.
#     """
#     today = date.today()
#     sensor_data = SensorReading.objects.filter(timestamp__date=today).order_by('timestamp')

#     if sensor_data.exists():
#         timestamps = [reading.timestamp.strftime("%H:%M") for reading in sensor_data]
#         water_levels = [reading.water_level for reading in sensor_data]
#         vibrations = [reading.vibration for reading in sensor_data]


#         # Get the latest water level as the current level
#         current_level = water_levels[-1]  # Using the last reading's water level
#     else:
#         timestamps = []
#         water_levels = []
#         vibrations = []
#         current_level = 0  # Default to 0 if no sensor data is available

#     context = {
#         'timestamps': timestamps,
#         'water_levels': water_levels,
#         'vibrations': vibrations,
#         'current_level': current_level,
#     }
#     return render(request, 'sensor/dashboard.html', context)

from datetime import date

@login_required
def dashboard(request):
    """
    Dashboard view that displays sensor data in graphical format.
    """
    today = date.today()
    sensor_data = SensorReading.objects.filter(timestamp__date=today).order_by('timestamp')

    if sensor_data.exists():
        timestamps = [reading.timestamp.strftime("%H:%M") for reading in sensor_data]
        water_levels = [reading.water_level for reading in sensor_data]
        vibrations = [reading.vibration for reading in sensor_data]

        # Calculate the current danger level from the sensor data
        current_level = water_levels[-1]  # Assume the latest reading for the danger level
    else:
        timestamps = []
        water_levels = []
        vibrations = []
        current_level = 0

    context = {
        'timestamps': timestamps,
        'water_levels': water_levels,
        'vibrations': vibrations,
        'current_level': current_level,  # Pass the danger level to the template
    }
    return render(request, 'sensor/dashboard.html', context)



@login_required
def notification_history(request):
    """
    View to display the logged-in user's notification history.
    """
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'sensor/notification_history.html', {'notifications': notifications})


@user_passes_test(lambda u: u.is_staff)
def send_custom_mail(request):
    """
    Admin view to send custom emails to users.
    """
    if request.method == 'POST':
        form = AdminMailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipients = User.objects.filter(is_staff=False).values_list('email', flat=True)

            # Send email to all non-admin users via Mailgun
            for recipient in recipients:
                result = send_simple_message(subject, message, recipient)
                # Handle the result (success or error) if needed
                print(result)  # For logging purposes, can be removed in production

            # Optionally, log this notification in the Notification model for each user
            for user in User.objects.filter(is_staff=False):
                Notification.objects.create(
                    recipient=user,
                    subject=subject,
                    message=message
                )

            return JsonResponse({'status': 'Emails sent successfully!'})
    else:
        form = AdminMailForm()
    return render(request, 'sensor/send_custom_mail.html', {'form': form})

# ------------------ Helper Function ------------------

def process_sensor_data(vibration, water_level):
    """
    Process sensor data to check for thresholds and validate with external APIs.
    Sends email notifications if necessary.
    """
    # Define thresholds
    VIBRATION_THRESHOLD = 1.0
    WATER_LEVEL_THRESHOLD = 2.0

    alert_message = ""
    if vibration > VIBRATION_THRESHOLD:
        alert_message += "High vibration levels detected.\n"
    if water_level > WATER_LEVEL_THRESHOLD:
        alert_message += "High water levels detected.\n"

    # Validate spikes with external APIs
    # Replace 'your_city' and 'your_api_key' with actual values
    WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather?q=Kathmandu&appid=853240a8b301521c232d6308ee74596d"
    USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"

    try:
        weather_response = requests.get(WEATHER_API_URL)
        weather_data = weather_response.json()

        usgs_response = requests.get(USGS_API_URL)
        usgs_data = usgs_response.json()

        # Example logic: Check if it's raining or if there's recent seismic activity
        if weather_data.get("weather") and any("rain" in condition.get("main", "").lower() for condition in weather_data["weather"]):
            alert_message += "Rain detected, increasing flood risk.\n"

        # Check if there have been recent earthquakes (you can refine this as needed)
        if usgs_data.get("features"):
            alert_message += "Recent seismic activity detected, increasing landslide risk.\n"

    except Exception as e:
        print(f"Error fetching external API data: {e}")

    # Save the sensor reading
    SensorReading.objects.create(
        water_level=water_level,
        vibration=vibration
    )

    # Send alert email if necessary using Mailgun
    if alert_message:
        subject = "Sensor Alert Notification"
        message = f"{alert_message}\nTimestamp: {datetime.now()}\n test "
        recipients = User.objects.filter(is_staff=False).values_list('email', flat=True)
        for recipient in recipients:
            result = send_simple_message(subject, message, recipient)
            # Handle the result (success or error) if needed
            print(result)  # For logging purposes, can be removed in production

        # Log notifications in the Notification model
        for user in User.objects.filter(is_staff=False):
            Notification.objects.create(
                recipient=user,
                subject=subject,
                message=message
            )

def landing_page(request):
   return render(request, 'sensor/landing_page.html')

def home(request):
   return render(request,'sensor/home.html')



import csv
from django.http import HttpResponse
from sensor.models import SensorReading  # Replace with your model

def export_to_csv(request):
    # Create the HTTP response with content type for CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sensor_data.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['User', 'Timestamp', 'Water Level', 'Vibration'])  # CSV Header

    # Fetch data from the database and write to CSV
    for obj in SensorReading.objects.all():
        writer.writerow([obj.user, obj.timestamp, obj.water_level, obj.vibration])

    return response



from django.utils.timezone import now, timedelta
from .models import SafetyLog

@login_required
def i_am_safe(request):
    """
    Logs a user's "I am Safe" response.
    """
    recent_timeframe = timedelta(minutes=5)  # Define the time frame to check recent logs
    recent_logs = SafetyLog.objects.filter(user=request.user, timestamp__gte=now() - recent_timeframe)

    if not recent_logs.exists():
        # Log the "I am Safe" click
        SafetyLog.objects.create(user=request.user)
        return JsonResponse({'status': 'Your status has been recorded. Thank you for confirming your safety.'})
    else:
        return JsonResponse({'status': 'Your safety has already been recorded recently.'})

@csrf_exempt
def send_rescue(request):
    """
    Sends a rescue car if no "I am Safe" log exists for the user in the recent mail timestamp.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')  # Expecting user_id in the POST data
            user = User.objects.get(id=user_id)
            recent_timeframe = timedelta(minutes=5)  # Define the time frame to check recent logs
            recent_logs = SafetyLog.objects.filter(user=user, timestamp__gte=now() - recent_timeframe)

            if not recent_logs.exists():
                # Logic to trigger rescue car
                # For example: Call another function to dispatch the car
                dispatch_rescue_car(user)
                return JsonResponse({'status': 'Rescue has been sent to your last known location.'})
            else:
                return JsonResponse({'status': 'User is safe. No rescue needed.'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid user ID.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def dispatch_rescue_car(user):
    """
    Placeholder for dispatching a rescue car.
    """
    # Example logic: Update the rescue car model or send a signal
    print(f"Rescue dispatched for user {user.username} at {now()}")
 