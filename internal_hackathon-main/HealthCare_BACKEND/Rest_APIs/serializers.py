from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import MyUser
from Data_user.models import DiabetesData
from django.db import IntegrityError
import random
import string 
from .utils import ml_generate_outcome
from .utils import extract_patient_details_from_image

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = MyUser
    fields=['username','first_name','phone', 'password', 'password2']
    extra_kwargs={
      'password':{'write_only':True},
      'username':{'read_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    phone = attrs.get('phone')
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validated_data):
    length = 12
    num_digits = random.randint((length // 2) + 1, length - 1)
    num_letters = length - num_digits
    digits = random.choices(string.digits, k=num_digits)
    letters = random.choices(string.ascii_uppercase, k=num_letters)
    username = ''.join(random.sample(digits + letters, k=length))
    validated_data['username'] = username


    #as we dont need this data after that 
    validated_data.pop('password2')
    return MyUser.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
  username = serializers.CharField(max_length=12)
  class Meta:
    model = MyUser
    fields = ['username', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = MyUser
    fields = ['username', 'first_name', 'phone','address',"role"]

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs
  
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs
    

### this is for disease specific data entry, for Diabetes 

class DiabetesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiabetesData
        fields = [
            'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
            'insulin', 'bmi', 'diabetes_pedigree_function', 'age', 'outcome', 'date_time',
        ]
        read_only_fields = ['date_time']

    def create(self, validated_data):
        user = self.context['request'].user
        diabetes_data = DiabetesData.objects.create(user=user, **validated_data)
        outcome = ml_generate_outcome(diabetes_data)
        diabetes_data.outcome = outcome
        diabetes_data.save()
        
        return diabetes_data
        

class OutcomeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiabetesData
        fields = ['outcome']
        read_only_fields = ['outcome']
    
    def update(self, instance, validated_data):
        instance.outcome = validated_data.get('outcome', instance.outcome)
        instance.save()
        return instance


# for GET request from user with role = 'doctor'

class PatientWithDiabetesDataSerializer(serializers.ModelSerializer):
    diabetes_records = DiabetesDataSerializer(many=True, read_only=True)
    user_id = serializers.CharField(source='username', read_only=True)

    class Meta:
        model = MyUser
        fields = ['id', 'user_id', 'first_name', 'phone', 'address', 'role', 'diabetes_records']

# for handling post, patch and delete request from doctor 

class UserWithDiabetesDataSerializer(serializers.ModelSerializer):
    diabetes_records = DiabetesDataSerializer(many=True, required=False)

    password = serializers.CharField(
        default="mypassword123",
        style={'input_type': 'password'},
        write_only=True
    )
    password2 = serializers.CharField(
        default="mypassword123",
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'phone', 'role', 'password', 'password2', 'diabetes_records']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False},
        }

    def validate(self, attrs):
        password = attrs.get('password', 'mypassword123')
        password2 = attrs.get('password2', 'mypassword123')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        return attrs

    def create(self, validated_data):
        username = validated_data.get('username')

        diabetes_records_data = validated_data.pop('diabetes_records', None)

        # Check if the user already exists
        user, created = MyUser.objects.get_or_create(username=username, defaults=validated_data)

        # If the user already exists, update their details
        if not created:
            for key, value in validated_data.items():
                setattr(user, key, value)
            user.save()

        # Create new diabetes records linked to the existing user
        if diabetes_records_data:
            for diabetes_record in diabetes_records_data:
                DiabetesData.objects.create(user=user, **diabetes_record)

        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.role = validated_data.get('role', instance.role)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()

        diabetes_records_data = validated_data.pop('diabetes_records', None)
        if diabetes_records_data:
            # Append new diabetes records to the existing ones
            for diabetes_record in diabetes_records_data:
                DiabetesData.objects.create(user=instance, **diabetes_record)

        return instance

    
# image extraction for doctor-serializer 

class PatientDetailsExtractionSerializer(serializers.Serializer):
    image = serializers.ImageField(write_only=True)
    
    patient_id = serializers.CharField(max_length=100, read_only=True)
    pregnancies = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    glucose = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    blood_pressure = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    skin_thickness = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    insulin = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    bmi = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    diabetes_pedigree_function = serializers.DecimalField(max_digits=5, decimal_places=3, read_only=True)
    age = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        image = attrs.get('image')
        extracted_data = extract_patient_details_from_image(image)
        attrs.update(extracted_data)
        return attrs

    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        default_password = 'mypassword123'

        user, created = MyUser.objects.get_or_create(
            username=patient_id,
            defaults={
                'first_name': 'Unknown',
                'phone': 'Unknown',
                'address': 'Unknown',
                'role': 'patient',
            }
        )

        if created:
            user.set_password(default_password)
            user.save()

        validated_data.pop('image')
        diabetes_data = DiabetesData.objects.create(user=user, **validated_data)
        diabetes_data.outcome = ml_generate_outcome(diabetes_data)
        diabetes_data.save()

        return DiabetesDataSerializer(diabetes_data).data

# ### this is for disease specific data entry, for Diabetes 

# class DiabetesDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiabetesData
#         fields = [
#             'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
#             'insulin', 'bmi', 'diabetes_pedigree_function', 'age', 'outcome', 'date_time',
#         ]
#         read_only_fields = ['date_time']

#     #check for final touch
#     #redundant - check and remove, Views has been changed already
#     def create(self, validated_data):

#         user = self.context['request'].user
#         diabetes_data = DiabetesData.objects.create(user=user, **validated_data)
#         outcome = ml_generate_outcome(diabetes_data)
#         diabetes_data['outcome'] = outcome
#         diabetes_data.save()
        
#         return diabetes_data
        

# class OutcomeUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiabetesData
#         fields = ['outcome']
#         read_only_fields = ['outcome']
    
#     def update(self, instance, validated_data):
#         instance.outcome = validated_data.get('outcome', instance.outcome)
#         instance.save()
#         return instance


# # for GET request from user with role = 'doctor'

# class PatientWithDiabetesDataSerializer(serializers.ModelSerializer):
#     diabetes_records = DiabetesDataSerializer(many=True, read_only=True)
#     user_id = serializers.CharField(source='username', read_only=True)

#     class Meta:
#         model = MyUser
#         fields = ['id','user_id', 'first_name', 'phone', 'address', 'role', 'diabetes_records']

# # for handling post, patch and delete request from doctor 

# class UserWithDiabetesDataSerializer(serializers.ModelSerializer):
#     diabetes_records = DiabetesDataSerializer(many=True, required=False)
    
#     password = serializers.CharField(
#         default="mypassword123",
#         style={'input_type': 'password'},
#         write_only=True
#     )
#     password2 = serializers.CharField(
#         default="mypassword123",
#         style={'input_type': 'password'},
#         write_only=True
#     )

#     class Meta:
#         model = MyUser
#         fields = ['username', 'first_name', 'phone', 'role', 'password', 'password2', 'diabetes_records']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'username': {'read_only': True},
#             'role': {'required': False},
#         }

#     def validate(self, attrs):
#         password = attrs.get('password', 'mypassword123')
#         password2 = attrs.get('password2', 'mypassword123')

#         if password != password2:
#             raise serializers.ValidationError("Password and Confirm Password don't match")

#         return attrs

#     def create(self, validated_data):
#         length = 12
#         num_digits = random.randint((length // 2) + 1, length - 1)
#         num_letters = length - num_digits
#         digits = random.choices(string.digits, k=num_digits)
#         letters = random.choices(string.ascii_uppercase, k=num_letters)
#         username = ''.join(random.sample(digits + letters, k=length))
#         validated_data['username'] = username

#         validated_data.pop('password2', None)

#         diabetes_records_data = validated_data.pop('diabetes_records', None)

#         user = MyUser.objects.create_user(**validated_data)

#         if diabetes_records_data:
#             for diabetes_record in diabetes_records_data:
#                 DiabetesData.objects.create(user=user, **diabetes_record)

#         return user

#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.phone = validated_data.get('phone', instance.phone)
#         instance.role = validated_data.get('role', instance.role)

#         password = validated_data.get('password')
#         if password:
#             instance.set_password(password)
#         instance.save()

#         diabetes_records_data = validated_data.pop('diabetes_records', None)
#         if diabetes_records_data:
#             DiabetesData.objects.filter(user=instance).delete()
#             for diabetes_record in diabetes_records_data:
#                 DiabetesData.objects.create(user=instance, **diabetes_record)

#         return instance
    

# # image extraction for doctor-serializer 

# class PatientDetailsExtractionSerializer(serializers.Serializer):
#     image = serializers.ImageField(write_only=True)
    
#     patient_id = serializers.CharField(max_length=100, read_only=True)
#     pregnancies = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
#     glucose = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
#     blood_pressure = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
#     skin_thickness = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
#     insulin = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
#     bmi = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
#     diabetes_pedigree_function = serializers.DecimalField(max_digits=5, decimal_places=3, read_only=True)
#     age = serializers.IntegerField(read_only=True)

#     def validate(self, attrs):
#         image = attrs.get('image')
#         extracted_data = extract_patient_details_from_image(image)
#         attrs.update(extracted_data)
#         return attrs

#     def create(self, validated_data):
#         patient_id = validated_data.pop('patient_id')
#         default_password = 'mypassword123'

#         user, created = MyUser.objects.get_or_create(
#             username=patient_id,
#             defaults={
#                 'first_name': 'Unknown',
#                 'phone': 'Unknown',
#                 'address': 'Unknown',
#                 'role': 'patient',
#             }
#         )

#         if created:
#             user.set_password(default_password)
#             user.save()

#         validated_data.pop('image')
#         diabetes_data = DiabetesData.objects.create(user=user, **validated_data)
#         diabetes_data.outcome = ml_generate_outcome(diabetes_data)
#         diabetes_data.save()

#         return DiabetesDataSerializer(diabetes_data).data
