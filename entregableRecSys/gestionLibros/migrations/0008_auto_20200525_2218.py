# Generated by Django 2.2.6 on 2020-05-25 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionLibros', '0007_auto_20200525_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='puntuacion',
            name='idUsuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionLibros.Usuario'),
        ),
        migrations.AlterField(
            model_name='puntuacion',
            name='isbn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionLibros.Libro'),
        ),
        migrations.AddField(
            model_name='libro',
            name='puntuaciones',
            field=models.ManyToManyField(through='gestionLibros.Puntuacion', to='gestionLibros.Usuario'),
        ),
    ]
