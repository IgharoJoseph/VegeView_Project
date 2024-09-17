from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'middle_name', 'gender', 'date_of_birth', 'organization', 'job_title', 'data_use')
    search_fields = ('user__username', 'user__email', 'organization', 'job_title')
