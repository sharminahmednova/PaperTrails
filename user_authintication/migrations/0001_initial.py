# Generated by Django 5.1.7 on 2025-04-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='laptop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=50)),
                ('re_pass', models.CharField(max_length=50)),
                ('laptop', models.CharField(max_length=50)),
                ('re_laptop', models.EmailField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('about', models.CharField(max_length=50)),
                ('textarea', models.CharField(max_length=50)),
                ('checkbox', models.CharField(max_length=50)),
                ('ram', models.IntegerField()),
            ],
        ),
    ]
