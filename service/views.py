from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from service.task import schedule_feedback_email
from .models import Appointments, Feedback
from .serializers import AppointmentsSerializer, FeedbackSerializer
import datetime
from .utils import add_event_to_google_calendar
# Create your views here.

class AppointmentsListCreate(generics.ListCreateAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentsSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        
        time_str = data.get('time')
        date_str = data.get('date')
        print(time_str)
        if date_str and time_str:
            try:
                start_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
            except ValueError:
                return Response({'error': 'Invalid date or time format.'}, status=status.HTTP_400_BAD_REQUEST)
        data['time'] = start_datetime

        serializer = AppointmentsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            # Add appointment to Google Calendar
            appointment = serializer.instance
            calendar_event_link = add_event_to_google_calendar(appointment)
         
            response_data = serializer.data
            if calendar_event_link:
                response_data['calendar_event_link'] = calendar_event_link
                schedule_feedback_email.delay(appointment.id)
            else:
                response_data['calendar_event_link'] = "Error creating Google Calendar event."


            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
