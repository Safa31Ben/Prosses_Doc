# Generated by Django 4.2 on 2023-04-11 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enseignant_candidat', '0003_rename_spécailité_condidat_specailite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamation',
            name='Reponse',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
