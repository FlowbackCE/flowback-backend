
# Generated by Django 3.1.2 on 2021-02-02 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210130_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
