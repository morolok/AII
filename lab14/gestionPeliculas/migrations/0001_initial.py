# Generated by Django 2.2.6 on 2020-05-25 10:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movieTitle', models.CharField(max_length=100)),
                ('releaseDate', models.DateField(blank=True, null=True)),
                ('releaseVideoDate', models.DateField(blank=True, null=True)),
                ('IMDbURL', models.URLField(validators=[django.core.validators.URLValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genreName', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupationName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1)),
                ('zipCode', models.CharField(max_length=8)),
                ('occupation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gestionPeliculas.Occupation')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rateDate', models.DateField(blank=True, null=True)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gestionPeliculas.Film')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gestionPeliculas.UserInformation')),
            ],
        ),
        migrations.AddField(
            model_name='film',
            name='genres',
            field=models.ManyToManyField(to='gestionPeliculas.Genre'),
        ),
        migrations.AddField(
            model_name='film',
            name='ratings',
            field=models.ManyToManyField(through='gestionPeliculas.Rating', to='gestionPeliculas.UserInformation'),
        ),
    ]
