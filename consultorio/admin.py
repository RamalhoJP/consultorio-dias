from django.contrib import admin
from .models import Paciente
from .models import Evento
from .models import Dentista

class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "idade")

admin.site.register(Paciente, PacienteAdmin)

class EventoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "descricao")

admin.site.register(Evento, EventoAdmin)

from django.contrib import admin
from .models import Dentista, Evento

class DentistaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "mostrar_eventos")  # Use o método customizado

    def mostrar_eventos(self, obj):
        # Recupere os eventos do dentista e mostre como string
        eventos = obj.eventos.all()  # Obtém todos os eventos relacionados ao dentista
        eventos_nomes = [evento.titulo for evento in eventos]  # Extraímos os títulos dos eventos
        return ", ".join(eventos_nomes) if eventos else "Nenhum evento"

    mostrar_eventos.short_description = "Eventos"  # Defina o nome que será exibido no admin

admin.site.register(Dentista, DentistaAdmin)
