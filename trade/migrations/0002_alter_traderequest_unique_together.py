# Generated by Django 5.2 on 2025-05-09 14:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0004_book_location'),
        ('trade', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='traderequest',
            unique_together={('sender', 'offered_book', 'requested_book')},
        ),
    ]
