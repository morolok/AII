# Generated by Django 2.2.6 on 2020-04-21 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionRecetas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receta',
            name='imagen',
            field=models.ImageField(upload_to='recetas', verbose_name='Imagen'),
        ),
    ]