# Generated by Django 5.0.4 on 2024-05-16 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_foto_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foto',
            name='foto',
            field=models.ImageField(upload_to=''),
        ),
    ]