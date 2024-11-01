from django.contrib import admin
from .models import Paciente

class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "idade")

admin.site.register(Paciente, PacienteAdmin)