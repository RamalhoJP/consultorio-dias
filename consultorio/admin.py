from django.contrib import admin
from .models import Orcamento
from .models import Cliente
from .models import Evento
from .models import Dentista

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "cpf")

admin.site.register(Cliente, ClienteAdmin)

class EventoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "descricao")

admin.site.register(Evento, EventoAdmin)

class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "preco", "pago")

admin.site.register(Orcamento, OrcamentoAdmin)

class DentistaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "mostrar_eventos")

    def mostrar_eventos(self, obj):
        eventos = obj.eventos.all()  
        eventos_nomes = [evento.titulo for evento in eventos]
        return ", ".join(eventos_nomes) if eventos else "Nenhum evento"

    mostrar_eventos.short_description = "Eventos"

admin.site.register(Dentista, DentistaAdmin)
