from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
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
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='projects')

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date.')

    # clean() is not automatically called when an object is saved, hence the overriding of save()
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Project, self).save(*args, **kwargs)


class Task(models.Model):
    CHOICES = (
        ('1', 'À commencer'),
        ('2', 'En cours'),
        ('3', 'Terminé'),
    )

    name = models.CharField(max_length=100, validators=[RegexValidator(
        r'^\S.*\S$', 'Name cannot start nor end with whitespace.')])
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField('Date de début')
    end_date = models.DateField('Date de fin')
    status = models.CharField(
        max_length=1, choices=CHOICES, default='Réunion')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks', blank=False)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if not (self.start_date == None or self.end_date == None):
            if not (self.start_date <= self.end_date):
                raise ValidationError(
                    'La date de début doit être antérieure à la date de fin.')

            if hasattr(self, 'project') and \
                    (self.start_date < self.project.start_date or self.end_date > self.project.end_date):
                raise ValidationError(
                    "Les dates d'une tâche ne peuvent pas dépasser les dates du projet")

class Meeting(models.Model):

    name = models.CharField(max_length=100, validators=[RegexValidator(
        r'^\S.*\S$', 'Name cannot start nor end with whitespace.')])
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField('Date de début')
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, default='Réunion')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='meetings', blank=False)

    def __str__(self):
        return self.name

class MyUser(AbstractUser):
    email = models.EmailField(validators=[EmailValidator(
        message="Please enter a valid email address.")])

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(MyUser, self).save(*args, **kwargs)
