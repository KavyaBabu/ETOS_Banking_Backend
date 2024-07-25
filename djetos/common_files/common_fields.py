from django.db import models


class CommonFieldsModel(models.Model):
    approval_status = models.CharField(max_length=2, null=True)
    approved_by = models.IntegerField(default=None, null=True)
    approved_on = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2)
    created_on = models.DateTimeField(default=None, null=True)
    created_by = models.IntegerField(default=None, null=True)
    updated_on = models.DateTimeField(default=None, null=True)
    updated_by = models.IntegerField(default=None, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
