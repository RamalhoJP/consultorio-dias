from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from .models import Evento
from .models import Dentista

def principal(request):
    template = loader.get_template('principal.html')
    return HttpResponse(template.render())

@login_required(login_url="/auth/login")
def agenda(request):
    template = loader.get_template('agenda.html')
    return HttpResponse(template.render())

@login_required(login_url="/auth/login")
def dentistas(request):
    dentistas = Dentista.objects.all()
    dentistas_json = []
    
    for dentista in dentistas:
        eventos = dentista.eventos.all()
        eventos_serializados = [
            {
                "id": evento.id,
                "titulo": evento.titulo,
                "data_inicio": evento.data_inicio.isoformat(),
                "data_fim": evento.data_fim.isoformat(),
                "descricao": evento.descricao,
            } for evento in eventos
        ]
        
        dentistas_json.append({
            "id": dentista.id,
            "nome": dentista.nome,
            "eventos": eventos_serializados,
        })
 
    return JsonResponse(dentistas_json, safe=False)

@login_required(login_url="/auth/login")
def eventos(request, dentista_id=None):
    if dentista_id:
        eventos = Evento.objects.filter(dentista_id=dentista_id)
    else:
        eventos = Evento.objects.all()

    eventos_json = [
        {
            "id": evento.id,
            "title": evento.titulo,
            "start": evento.data_inicio.isoformat(),
            "end": evento.data_fim.isoformat(),
            "description": evento.descricao,
        } for evento in eventos
    ]
    
    return JsonResponse(eventos_json, safe=False)

@csrf_exempt
@login_required(login_url="/auth/login")
def cadastrar_evento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            evento_id = data.get('id')
            titulo = data.get('titulo')
            descricao = data.get('descricao')
            data_inicio = data.get('data_inicio')
            data_fim = data.get('data_fim')
            dentista_id = data.get('dentista')  

            dentista = Dentista.objects.get(id=dentista_id)

            if evento_id: 
                evento = Evento.objects.get(id=evento_id)
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_inicio = data_inicio
                evento.data_fim = data_fim
                evento.dentista = dentista
                evento.save()
            else: 
                Evento.objects.create(
                    titulo=titulo,
                    descricao=descricao,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    dentista=dentista 
                )

            return JsonResponse({"status": "success"})

        except Dentista.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Dentista não encontrado!"}, status=400)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
@login_required(login_url="/auth/login")
def atualizar_evento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            evento = Evento.objects.get(id=data['id'])
            evento.data_inicio = data['data_inicio']
            evento.data_fim = data['data_fim']
            evento.save()
            return JsonResponse({"status": "success"})
        except Evento.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Evento não encontrado."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
@login_required(login_url="/auth/login")
def deletar_evento(request, evento_id):
    if request.method == 'DELETE':
        try:
            evento = Evento.objects.get(id=evento_id)
            evento.delete()
            return JsonResponse({"status": "success", "message": "Evento deletado com sucesso!"})
        except Evento.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Evento não encontrado!"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Método não permitido!"}, status=405)
