# Generated by Django 5.0.4 on 2024-05-28 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_alter_receta_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receta',
            name='pasos',
            field=models.CharField(max_length=5000),
        ),
    ]
