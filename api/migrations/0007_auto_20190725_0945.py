# Generated by Django 2.2.3 on 2019-07-25 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190718_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='value',
            field=models.CharField(max_length=30),
        ),
    ]