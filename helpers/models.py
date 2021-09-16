from django.db import models


class TrackingModel(models.Model):
    """Model definition for TrackingModel."""
    created_at=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for TrackingModel."""
        abstract=True
        ordering=('-created_at')
