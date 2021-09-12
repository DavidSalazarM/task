from django.db import models


class MainTable(models.Model):
    date_and_time_attention = models.DateTimeField(null=False, blank=False)
    end_time_attention = models.TimeField(null=False, blank=False)
    company = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    answer = models.TextField(null=False, blank=True)
    application_date = models.DateField(null=False, blank=False)
