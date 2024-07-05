from rest_framework import serializers
from .models import Appointments, Feedback


class AppointmentsSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField()
    class Meta:
        model = Appointments
        fields = '__all__'
        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
                                