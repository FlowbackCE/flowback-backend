
# Generated by Django 3.1.2 on 2021-02-02 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210202_0106'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='website',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
