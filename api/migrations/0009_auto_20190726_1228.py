# Generated by Django 2.2.3 on 2019-07-26 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190726_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadata',
            name='value',
            field=models.CharField(max_length=100),
        ),
    ]
