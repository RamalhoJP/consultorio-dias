from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)
    dentista = models.ForeignKey('Dentista', on_delete=models.CASCADE, related_name='eventos', null=True)

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, null=True)
    telefone = models.TextField(blank=True, null=True)

class Dentista(models.Model):
    nome = models.CharField(max_length=255)

class Procedimento(models.Model):
    nome = models.CharField(max_length=255)
    finalizado = models.BooleanField(default=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateField()
    data_finalizado = models.DateField()
    
class Orcamento(models.Model):
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anaminesia = models.BooleanField(default=False)
    dentes_com_circulo = models.JSONField(default=list)
    dentes_com_risco = models.JSONField(default=list)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='orcamentos', default=None, null=True, blank=True)
    procedimentos = models.ForeignKey(Procedimento, on_delete=models.CASCADE, related_name='orcamentos', default=None, null=True, blank=True)
    datas = models.JSONField(default=list,null=True, blank=True)