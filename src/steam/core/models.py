from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


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
            raise ValidationError(
                'La date de début doit être antérieure à la date de fin.')

    # clean() is not automatically called when an object is saved, hence the overriding of save()
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Project, self).save(*args, **kwargs)


@receiver(m2m_changed, sender=Project.members.through)
def disallow_owner_as_member(sender, **kwargs):
    action = kwargs.get('action', None)
    if action == 'pre_add':
        owner = kwargs.get('instance').owner
        new_members = kwargs.get('pk_set', [])
        if owner.pk in new_members:
            raise ValidationError("Owner cannot be added as a member.")
