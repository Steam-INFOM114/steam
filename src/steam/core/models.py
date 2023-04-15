from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date.')

    # clean() is not automatically called when an object is saved, hence the overriding of save()
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Project, self).save(*args, **kwargs)


class MyUser(AbstractUser):
    email = models.EmailField(validators=[EmailValidator(message="Please enter a valid email address.")])

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(MyUser, self).save(*args, **kwargs)

