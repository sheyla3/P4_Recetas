# Generated by Django 5.0.4 on 2024-05-15 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_admin_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
