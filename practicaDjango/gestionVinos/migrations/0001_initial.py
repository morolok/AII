# Generated by Django 2.2.6 on 2020-05-11 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=1024, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Denominacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=1024, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Uva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=1024, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Vino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=1024, verbose_name='Nombre')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('bodega', models.TextField(verbose_name='Bodega')),
                ('denominacion', models.TextField(verbose_name='Denomicación de origen')),
                ('puntuacion', models.DecimalField(decimal_places=1, max_digits=10, null=True, verbose_name='Puntuación')),
                ('uvas', models.ManyToManyField(to='gestionVinos.Uva')),
            ],
        ),
    ]
