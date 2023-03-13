from django.db import models


class ReportedPhoneNumber(models.Model):
    phone_number = models.CharField(max_length=20)
    report_date = models.DateField(auto_now_add=True)
    reported_phone_number_count = models.IntegerField(default=0)

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only increment count on creation, not on update
            self.reported_phone_number_count = Report.objects.filter(reported_phone_number=self).count()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.phone_number

class Report(models.Model):
    reported_phone_number = models.ForeignKey(ReportedPhoneNumber, on_delete=models.CASCADE, related_name='reports')

