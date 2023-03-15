from django.contrib import admin
from .models import ReportedPhoneNumber

@admin.register(ReportedPhoneNumber)
class ReportedPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'report_date', 'reported_phone_number_count')
