from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, username,first_name, phone, role='patient', password=None, password2=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            username=username,
            first_name = first_name,
            phone = phone,
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username=username,
            role='doctor',  # Set role for superuser
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(verbose_name='user id ',max_length=12,unique=True,)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'username'  # Use 'username' as the primary identifier
    REQUIRED_FIELDS = []  # You can add other required fields here if needed

    objects = MyUserManager()

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ('can_add_users', 'Can add users'),
            ('can_view_users', 'Can view users'),
            ('can_update_users', 'Can update users'),
            ('can_delete_users', 'Can delete users'),
        ]

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin