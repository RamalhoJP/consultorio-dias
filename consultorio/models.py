from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)
    dentista = models.ForeignKey('Dentista', on_delete=models.CASCADE, related_name='eventos', null=True)

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.TextField(blank=True, null=True)

class Dentista(models.Model):
    nome = models.CharField(max_length=255)

class Orcamento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=1000)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    dentes_com_circulo = models.JSONField(default=list)
    dentes_com_risco = models.JSONField(default=list)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='orcamentos', null=True)
    