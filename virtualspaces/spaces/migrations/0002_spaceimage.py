# Generated by Django 2.1.3 on 2018-11-20 06:42

from django.db import migrations, models
import django.db.models.deletion
import virtualspaces.spaces.models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to=virtualspaces.spaces.models.get_space_image_upload_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(default=0)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='space_images', to='spaces.Space')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]