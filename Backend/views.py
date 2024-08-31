from .models import MyUser
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound


# generates token for user
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      user = serializer.save()
      token = get_tokens_for_user(user)
      return Response({'token':token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      username = serializer.data.get('username')
      password = serializer.data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Username or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

### views and logic for patient to view his dashboard

class GetDiabetesDataView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        diabetes_data = DiabetesData.objects.filter(user=request.user)
        serializer = DiabetesDataSerializer(diabetes_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# implement the ml logic later 
def ml_generate_outcome(data):
   pass

class DiabetesDataView(APIView):
    
    def post(self, request):
        serializer = DiabetesDataSerializer(data=request.data)
        if serializer.is_valid():
            diabetes_data = serializer.save()

            # Assume `ml_generate_outcome` is the function that triggers your ML logic
            # and returns the outcome. This is where you implement the async handling.
            outcome = ml_generate_outcome(diabetes_data)  # This could be an async call

            # Update the outcome field
            outcome_serializer = OutcomeUpdateSerializer(diabetes_data, data={'outcome': outcome})
            if outcome_serializer.is_valid():
                outcome_serializer.save()
                return Response(outcome_serializer.data, status=status.HTTP_201_CREATED)

            return Response(outcome_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
### views and logic for Doctor to view dashboard of his patients

class PatientDataView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.role != 'doctor':
            raise PermissionDenied("You do not have permission to perform this action.")
        patients = MyUser.objects.filter(role='patient').prefetch_related('diabetes_records')
        serializer = PatientWithDiabetesDataSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.role != 'doctor':
            raise PermissionDenied("You do not have permission to perform this action.")
        serializer = UserWithDiabetesDataSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()

            # Assuming you have a function to calculate the outcome
            for diabetes_data in user.diabetes_records.all():
                diabetes_data.outcome = self.calculate_outcome(diabetes_data)
                diabetes_data.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        if request.user.role != 'doctor':
            raise PermissionDenied("You do not have permission to perform this action.")
        try:
            diabetes_data = DiabetesData.objects.get(pk=pk)
        except DiabetesData.DoesNotExist:
            raise NotFound("Diabetes data not found.")
        
        serializer = UserWithDiabetesDataSerializer(diabetes_data, data=request.data, context={'request': request})
        if serializer.is_valid():
            diabetes_data = serializer.save()

            # Recalculate the outcome after updating
            diabetes_data.outcome = self.calculate_outcome(diabetes_data)
            diabetes_data.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if request.user.role != 'doctor':
            raise PermissionDenied("You do not have permission to perform this action.")
        try:
            diabetes_data = DiabetesData.objects.get(pk=pk)
        except DiabetesData.DoesNotExist:
            raise NotFound("Diabetes data not found.")
        diabetes_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def calculate_outcome(self, diabetes_data):
        # Replace this with your machine learning logic
        # Example: return some_ml_model.predict(diabetes_data)
        return 1  # Just a placeholder
