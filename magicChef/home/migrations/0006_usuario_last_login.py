# Generated by Django 5.0.4 on 2024-05-09 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_usuario_correo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
