# Generated by Django 3.2.18 on 2023-04-18 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_myuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='key',
            field=models.CharField(default='', editable=False, max_length=5, unique=True),
        ),
    ]
