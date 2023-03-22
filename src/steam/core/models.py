from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_projects')
    members = models.ManyToManyField(User, related_name='projects', blank=True)

    def __str__(self):
        return self.name

    # TODO: localization of validation errors
    def clean(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError('La date de début doit être antérieure à la date de fin.')

    # clean() is not automatically called when an object is saved, hence the overriding of save()
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Project, self).save(*args, **kwargs)
