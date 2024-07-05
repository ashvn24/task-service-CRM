from django.db import models

# Create your models here.

Time ={
    ('09:00', '09:00'),
    ('10:00', '10:00'),
    ('11:00', '11:00'),
    ('12:00', '12:00'),
    ('13:00', '13:00'),
    ('14:00', '14:00'),
    ('15:00', '15:00'),
    ('16:00', '16:00'),
    ('17:00', '17:00'),
}

class Appointments(models.Model):
    user_id = models.IntegerField()
    booking = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField(choices=Time, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def meta(self):
        ordering = ['created_at']
        verbose_name = 'Appointment'
        
class Feedback(models.Model):
    appointment= models.ForeignKey(Appointments, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def meta(self):
        ordering = ['created_at']
        verbose_name = 'Feedback'
        