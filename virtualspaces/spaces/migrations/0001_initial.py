# Generated by Django 2.1.3 on 2018-11-20 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('hourly_rate', models.IntegerField(blank=True, null=True)),
                ('daily_rate', models.IntegerField(blank=True, null=True)),
                ('min_booking_hours', models.IntegerField(blank=True, null=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(0, 'Not Submitted'), (1, 'Awaiting Listing Approval'), (2, 'Listing Approved')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
