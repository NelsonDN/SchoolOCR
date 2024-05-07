# Generated by Django 5.0.3 on 2024-05-07 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schoolmanage', '0007_eleve_filiere'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Nom')),
                ('slug', models.CharField(max_length=64, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Filière',
                'verbose_name_plural': 'Filières',
            },
        ),
        migrations.CreateModel(
            name='Filiere_Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Note minimal')),
                ('filiere_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orientation.filiere')),
                ('matiere_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolmanage.matiere')),
            ],
        ),
        migrations.AddField(
            model_name='filiere',
            name='matiere',
            field=models.ManyToManyField(through='orientation.Filiere_Matiere', to='schoolmanage.matiere'),
        ),
    ]
