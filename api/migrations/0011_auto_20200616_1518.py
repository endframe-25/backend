# Generated by Django 3.0.2 on 2020-06-16 15:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200616_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='resturants',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 15, 18, 37, 251397, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 15, 18, 37, 250785, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 15, 18, 37, 248695, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storerestro',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 15, 18, 37, 250081, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tax',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 15, 18, 37, 252027, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='services',
            field=models.CharField(default='NA', max_length=256),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 15, 18, 37, 245953, tzinfo=utc)),
        ),
    ]
