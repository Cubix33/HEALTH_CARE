from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from Data_user.models import DiabetesData

class MyUserModelAdmin(BaseUserAdmin):
  list_display = ('id', 'username', 'is_admin','role','created_at','updated_at')
  list_filter = ('is_admin','role')
  fieldsets = (
      ('User Credentials', {'fields': ('username', 'password')}),
      ('Personal info', {'fields': ('first_name','last_name','phone','role')}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('username','password1', 'password2','first_name','last_name','phone','address','role', 'is_admin'),
      }),
  )
  search_fields = ('username',)
  ordering = ('username', 'created_at')
  filter_horizontal = ()


class DiabetesDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age', 'outcome')
    search_fields = ('user__username', 'user__first_name', 'user__phone', 'outcome')
    list_filter = ('outcome', 'glucose', 'bmi', 'age')
    readonly_fields = ('date_time',)


# Register the new UserAdmin...
admin.site.register(MyUser, MyUserModelAdmin)
admin.site.register(DiabetesData, DiabetesDataAdmin)