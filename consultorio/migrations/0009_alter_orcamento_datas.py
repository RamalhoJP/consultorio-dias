# Generated by Django 5.1.2 on 2024-12-12 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultorio', '0008_procedimento_remove_orcamento_descricao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='datas',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]