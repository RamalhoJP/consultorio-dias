from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)
    dentista = models.ForeignKey('Dentista', on_delete=models.CASCADE, related_name='eventos', null=True)

class Paciente(models.Model):
    nome = models.CharField(max_length=255)
    idade = models.IntegerField()

class Dentista(models.Model):
    nome = models.CharField(max_length=255)
