# Generated by Django 5.1.2 on 2025-01-01 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultorio', '0013_remove_evento_descricao_evento_cliente_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='Cliente',
            new_name='cliente',
        ),
    ]
