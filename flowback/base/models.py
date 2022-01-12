from django.db import models


class TimeStampedModel(models.Model):
    """
    This model is used for record the created and modified date of any record.
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
