import secrets
from django.db import models

class ProtectedLink(models.Model):
    original_url = models.URLField()
    device_limit = models.PositiveIntegerField()
    token = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        super().save(*args,**kwargs)

class Device(models.Model):
    link = models.ForeignKey(ProtectedLink,on_delete=models.CASCADE)
    fingerprint = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('link','fingerprint')
