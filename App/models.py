from django.db import models


class ReportedPhoneNumber(models.Model):
    phone_number = models.CharField(max_length=20)
    report_date = models.DateField(auto_now_add=True)
    reporter_name = models.CharField(max_length=100)
    report_description = models.TextField()

    def __str__(self):
        return self.phone_number
