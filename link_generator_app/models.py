import secrets
from django.db import models

class ProtectedLink(models.Model):
    original_url = models.URLField()
    device_limit = models.PositiveIntegerField()
    token = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.original_url


class Device(models.Model):
    link = models.ForeignKey(ProtectedLink, on_delete=models.CASCADE)
    fingerprint = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.link.token} - {self.fingerprint[:8]}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['link', 'fingerprint'],
                name='unique_device_per_link'
            )
        ]