# Generated by Django 5.0.4 on 2024-06-04 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_receta_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='apodo',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
