
# Generated by Django 3.1.2 on 2021-02-11 23:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210209_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupdocs',
            name='doc_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=256),
            preserve_default=False,
        ),
    ]
