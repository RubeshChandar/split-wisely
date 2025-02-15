from django.db import models
from users.models import CustomUser

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(CustomUser, related_name="enrolledgroups")
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
