# Generated by Django 4.2 on 2023-04-11 06:32

import Enseignant_candidat.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Gestion', '0001_initial'),
        ('Enseignant_candidat', '0001_initial'),
        ('Administrative_staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condidat',
            fields=[
                ('id_condidat', models.OneToOneField(db_column='id_condidat', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('universite', models.CharField(max_length=200)),
                ('code_anonyme', models.CharField(db_index=True, max_length=25, null=True, unique=True)),
                ('spécailité', models.CharField(db_index=True, max_length=25)),
                ('id_concours', models.OneToOneField(db_column='id_concours', on_delete=django.db.models.deletion.CASCADE, to='Administrative_staff.concours')),
            ],
            options={
                'db_table': 'condidat',
            },
        ),
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('id_enseignant', models.OneToOneField(db_column='id_enseignant', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('grade', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'enseignant',
            },
        ),
        migrations.CreateModel(
            name='These',
            fields=[
                ('id_these', models.AutoField(primary_key=True, serialize=False)),
                ('sujet', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('id_enseignant', models.OneToOneField(db_column='id_enseignant', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.enseignant')),
            ],
            options={
                'db_table': 'these',
            },
        ),
        migrations.CreateModel(
            name='Reclamation',
            fields=[
                ('id_reclamation', models.AutoField(primary_key=True, serialize=False)),
                ('contenu', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now=True)),
                ('Reponse', models.CharField(max_length=500)),
                ('id_condidat', models.OneToOneField(db_column='id_condidat', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.condidat')),
            ],
            options={
                'db_table': 'reclamation',
            },
        ),
        migrations.CreateModel(
            name='Notification_Enseignants',
            fields=[
                ('id_notification_enseignant', models.AutoField(primary_key=True, serialize=False)),
                ('contenu', models.CharField(max_length=500)),
                ('date_notification', models.DateTimeField(auto_now=True)),
                ('id_enseignant', models.OneToOneField(db_column='id_enseignant', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.enseignant')),
            ],
            options={
                'db_table': 'notification_enseignants',
            },
        ),
        migrations.CreateModel(
            name='Notification_Condidats',
            fields=[
                ('id_notification_condidat', models.AutoField(primary_key=True, serialize=False)),
                ('contenu', models.CharField(max_length=500)),
                ('date_notification', models.DateTimeField(auto_now=True)),
                ('id_condidat', models.OneToOneField(db_column='id_condidat', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.condidat')),
            ],
            options={
                'db_table': 'notification_condidats',
            },
        ),
        migrations.AddField(
            model_name='choix',
            name='id_condidat',
            field=models.OneToOneField(db_column='id_condidat', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.condidat'),
        ),
        migrations.AddField(
            model_name='choix',
            name='id_these',
            field=models.OneToOneField(db_column='id_these', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.these'),
        ),
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat_presence', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('id_condidat', models.OneToOneField(db_column='id_condidat', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.condidat')),
                ('id_enseignant', models.OneToOneField(db_column='id_enseignant', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.enseignant')),
            ],
            options={
                'db_table': 'presence',
                'unique_together': {('id_enseignant', 'id_condidat')},
            },
        ),
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.FloatField(default=0.0, validators=[Enseignant_candidat.models.validate_decimals])),
                ('numero_de_correction', models.IntegerField(choices=[(1, '1er'), (2, '2éme'), (3, '3éme')])),
                ('code_anonyme_condidat', models.OneToOneField(db_column='code_anonyme_condidat', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.condidat', to_field='code_anonyme')),
                ('id_enseignant', models.OneToOneField(db_column='id_enseignant', on_delete=django.db.models.deletion.CASCADE, to='Enseignant_candidat.enseignant')),
            ],
            options={
                'db_table': 'correction',
                'unique_together': {('id_enseignant', 'code_anonyme_condidat')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='choix',
            unique_together={('id_these', 'id_condidat')},
        ),
    ]
