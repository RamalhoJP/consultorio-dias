# Generated by Django 5.1.2 on 2024-12-11 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultorio', '0006_orcamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(max_length=14, null=True),
        ),
    ]