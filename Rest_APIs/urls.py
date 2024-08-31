from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView
from .views import GetDiabetesDataView, PatientDataView, DoctorPatientListView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    # add log-out feature here

    #end point for patients 
    path('get-diabetes-data/', GetDiabetesDataView.as_view(), name='get-diabetes-data'),

    # Endpoints for doctors
    path('doctor/patients/', DoctorPatientListView.as_view(), name='doctor_patient_list'),
    
    # Endpoints for patient-specific operations
    path('patients/', PatientDataView.as_view(), name='patient_list_create'),
    path('patients/<int:pk>/', PatientDataView.as_view(), name='patient_detail_update_delete'),
]
