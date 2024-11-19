# Generated by Django 5.1.2 on 2024-11-16 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultorio', '0003_dentista_evento_dentista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='dentista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='consultorio.dentista'),
        ),
    ]
