from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('agenda/', views.agenda, name='agenda'),

    path('clientes/', views.clientes, name='listar_clientes'),
    path('clientes/cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:cliente_id>/', views.excluir_cliente, name='excluir_cliente'),

    path('dentistas/', views.dentistas, name='dentistas'),
    path('dentistas/cadastrar', views.cadastrar_dentista, name='cadastrar_dentista'),

    path('events/', views.eventos, name='events'),
    path('events/<int:dentista_id>/', views.eventos, name='events_by_dentista'),
    path('cadastrar_evento/', views.cadastrar_evento, name='cadastrar_evento'),
    path('atualizar_evento/', views.atualizar_evento, name='atualizar_evento'),
    path('deletar_evento/<int:evento_id>/', views.deletar_evento, name='deletar_evento'),
    
    path('cadastrar-orcamento/', views.cadastrar_orcamento, name='cadastrar_orcamento'),
    path('listar-orcamentos/', views.listar_orcamentos, name='listar_orcamentos'),
    path('orcamento/editar/<int:id>/', views.editar_orcamento, name='editar_orcamento'),
    path('orcamento/excluir/<int:id>/', views.excluir_orcamento, name='excluir_orcamento'),
]