
# Generated by Django 3.1.2 on 2021-02-15 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20210213_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='poll_request',
            field=models.CharField(choices=[('direct_join', 'Direct Join'), ('need_moderation', 'Needs Moderation')], default='direct_join', max_length=50, verbose_name='Poll Request Type'),
        ),
    ]
