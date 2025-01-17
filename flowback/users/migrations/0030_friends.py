
# Generated by Django 3.1.2 on 2021-03-14 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_group_room_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('room_name', models.CharField(max_length=100)),
                ('request_accept', models.BooleanField(default=False)),
                ('request_accepted_at', models.DateTimeField(blank=True, null=True)),
                ('request_sent_at', models.DateTimeField(auto_now_add=True)),
                ('block', models.BooleanField(default=False)),
                ('user_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_sender', to=settings.AUTH_USER_MODEL)),
                ('user_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
