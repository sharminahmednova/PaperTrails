# Generated by Django 5.2 on 2025-04-26 04:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_book_condition'),
        ('user_authintication', '0004_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='allow_bidding',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='user_authintication.profile')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='pages.book')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='pages.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='user_authintication.profile')),
            ],
            options={
                'unique_together': {('user', 'book')},
            },
        ),
    ]
