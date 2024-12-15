# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.landing_page, name='landing_page'),
#     path('home/',views.home, name='home'),
#     path('register/', views.register, name='register'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='logout'),
#     path('sensor-input/', views.sensor_input, name='sensor_input'),
#     path('notifications/', views.notification_history, name='notification_history'),
#     path('api/sensor-input/', views.sensor_data_input, name='sensor_data_input'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('send-notification/', views.admin_notification, name='admin_notification'),
#     path('api/submit-data/', views.submit_sensor_data, name='submit_sensor_data'),
# ]

# sensor/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Landing Page
    path('home/', views.home, name='home'),             # Home Page after login
    path('register/', views.register, name='register'),  # User Registration
    path('login/', views.user_login, name='login'),      # User Login
    path('logout/', views.user_logout, name='logout'),   # User Logout
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard
    path('notifications/', views.notification_history, name='notification_history'),  # Notification History
    path('send-custom-mail/', views.send_custom_mail, name='send_custom_mail'),  # Admin Send Mail
    path('api/sensor-data/', views.receive_sensor_data, name='receive_sensor_data'),  # ESP Data Endpoint
    path('export/', views.export_to_csv, name='export_to_csv'),
    path('i-am-safe/', views.i_am_safe, name='i_am_safe'),
    path('send-rescue/', views.send_rescue, name='send_rescue'),
]
