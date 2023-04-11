import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.validators import RegexValidator, EmailValidator
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='projects', blank=True)
    key = models.CharField(max_length=5, unique=True, default='', editable=False)

    def __str__(self):
        return self.name

    # TODO: localization of validation errors
    def clean(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError(
                'La date de début doit être antérieure à la date de fin.')

        if self.id and self.owner in self.members.all():
            raise ValidationError('Owner cannot also be a project member')

    # clean() is not automatically called when an object is saved, hence the overriding of save()
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        self.full_clean()
        super(Project, self).save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        """Generate a unique random string of 5 characters for the 'key' field in the 'Project' model."""
        while True:
            generated_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if not cls.objects.filter(key=generated_key).exists():
                return generated_key

@receiver(m2m_changed, sender=Project.members.through)
def disallow_owner_as_member(sender, **kwargs):
    action = kwargs.get('action', None)
    if action == 'pre_add':
        owner = kwargs.get('instance').owner
        new_members = kwargs.get('pk_set', [])
        if owner.pk in new_members:
            raise ValidationError("Owner cannot be added as a member.")


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
        max_length=1, choices=CHOICES, default='À commencer')
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


class MyUser(AbstractUser):
    email = models.EmailField(validators=[EmailValidator(
        message="Please enter a valid email address.")],
        unique=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Project, self).save(*args, **kwargs)


class Task(models.Model):
    CHOICES = (
        ('1', 'À commencer'),
        ('2', 'En cours'),
        ('3', 'Terminé'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date  = models.DateField('Date de début')
    end_date = models.DateField('Date de fin')
    status = models.CharField(max_length=1, choices=CHOICES, default='À commencer')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')


    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if not (self.start_date == None or self.end_date == None):
            if not (self.start_date <= self.end_date):
                raise ValidationError('La date de début doit être antérieure à la date de fin.')
