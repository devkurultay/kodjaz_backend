# Generated by Django 4.1.4 on 2023-01-07 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0011_rename_output_submission_console_output_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_created', models.DateTimeField(auto_now_add=True, verbose_name='Subscription Date and Time')),
                ('date_time_modified', models.DateTimeField(auto_now=True, verbose_name='Subscription Modification Date and Time')),
                ('track', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='subscription', to='courses.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_subscription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
