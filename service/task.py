# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Appointments
from datetime import datetime, timedelta

@shared_task
def schedule_feedback_email(appointment_id):
    try:
        appointment = Appointments.objects.get(id=appointment_id)
        appointment_datetime = datetime.combine(appointment.date, appointment.time)
        print(appointment_datetime,'-------------------')
        # Calculate the time 2 hours after the appointment datetime
        send_time = appointment_datetime + timedelta(minutes=2)
        print(send_time,'-------------------')
        # Schedule feedback email to be sent at send_time
        send_feedback_email.apply_async((appointment.email,), eta=send_time)
    except Appointments.DoesNotExist:
        pass  

@shared_task
def send_feedback_email(user_email):
    
    print("Sending feedback email to", user_email)
    # Send feedback email logic
    # send_mail(
    #     'Feedback Request',
    #     'Please provide feedback on your recent appointment.',
    #     'from@example.com',
    #     [user_email],
    #     fail_silently=False,
    # )
