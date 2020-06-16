# Generated by Django 3.0.2 on 2020-06-16 14:44

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200616_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='serves',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.cat'),
        ),
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 14, 44, 47, 512486, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 14, 44, 47, 511858, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 14, 44, 47, 510106, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='storerestro',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 14, 44, 47, 511195, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tax',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 14, 44, 47, 513114, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 14, 44, 47, 507983, tzinfo=utc)),
        ),
    ]
