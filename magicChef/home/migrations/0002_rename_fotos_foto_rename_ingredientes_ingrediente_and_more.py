# Generated by Django 5.0.4 on 2024-04-25 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Fotos',
            new_name='Foto',
        ),
        migrations.RenameModel(
            old_name='Ingredientes',
            new_name='Ingrediente',
        ),
        migrations.RenameModel(
            old_name='Usuarios',
            new_name='Usuario',
        ),
        migrations.RenameModel(
            old_name='Recetas',
            new_name='Receta',
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id_comentario', models.AutoField(primary_key=True, serialize=False)),
                ('comentario', models.CharField(max_length=500)),
                ('calificacion', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('id_receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.receta')),
            ],
        ),
        migrations.DeleteModel(
            name='Comentarios',
        ),
    ]