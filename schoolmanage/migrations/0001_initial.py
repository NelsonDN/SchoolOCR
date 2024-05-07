# Generated by Django 5.0.3 on 2024-04-04 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Nom')),
            ],
            options={
                'verbose_name': 'Cycle',
                'verbose_name_plural': 'Cycles',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Nom')),
            ],
            options={
                'verbose_name': 'Evaluation',
                'verbose_name_plural': 'Evaluations',
            },
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Nom')),
            ],
            options={
                'verbose_name': 'Matière',
                'verbose_name_plural': 'Matières',
            },
        ),
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Nom')),
                ('effectif', models.IntegerField(verbose_name='Effectif')),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schoolmanage.cycle', verbose_name='Cycle')),
            ],
            options={
                'verbose_name': 'Classe',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Nom')),
                ('matricule', models.CharField(max_length=64, unique=True, verbose_name='Matricule')),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='schoolmanage.classe', verbose_name='Classe')),
            ],
            options={
                'verbose_name': 'Eleve',
                'verbose_name_plural': 'Eleves',
            },
        ),
        migrations.CreateModel(
            name='Classe_Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient', models.IntegerField(default=1, verbose_name='Coefficient')),
                ('classe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolmanage.classe')),
                ('matiere_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolmanage.matiere')),
            ],
        ),
        migrations.AddField(
            model_name='classe',
            name='matiere',
            field=models.ManyToManyField(through='schoolmanage.Classe_Matiere', to='schoolmanage.matiere'),
        ),
    ]