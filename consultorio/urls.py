from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('agenda/', views.agenda, name='agenda'),
    path('events/', views.eventos, name='events'),
    path('events/<int:dentista_id>/', views.eventos, name='events_by_dentista'),
    path('cadastrar_evento/', views.cadastrar_evento, name='cadastrar_evento'),
    path('atualizar_evento/', views.atualizar_evento, name='atualizar_evento'),
    path('deletar_evento/<int:evento_id>/', views.deletar_evento, name='deletar_evento'),
    path('dentistas/', views.dentistas, name='dentistas'),
]