# Generated by Django 5.1.3 on 2024-11-21 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0002_notification_subject_alter_sensorreading_timestamp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('recipient', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
