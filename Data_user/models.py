from Rest_APIs.models import MyUser
from django.db import models

class DiabetesData(models.Model):
    ''' name, phone and date are already present in the user database
    
    # name = models.CharField(max_length=53, null=True, blank=True)
    # phone_no = models.CharField(max_length=50, null=True, blank=True) 
    # date = models.CharField(max_length=10, null=True, blank=True)
    '''

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='diabetes_records')
    pregnancies = models.IntegerField(null=True, blank=True)
    glucose = models.IntegerField(null=True, blank=True)
    blood_pressure = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skin_thickness = models.IntegerField(null=True, blank=True)
    insulin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    diabetes_pedigree_function = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    outcome = models.IntegerField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name}, your report outcome is: {self.outcome}"
