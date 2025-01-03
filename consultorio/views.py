from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from .models import Evento, Dentista, Cliente, Orcamento, Procedimento
from datetime import datetime

def principal(request):
    template = loader.get_template('principal.html')
    return HttpResponse(template.render())

@login_required(login_url="/auth/login")
def listar_orcamentos(request):
    orcamentos = Orcamento.objects.all().order_by('cliente__nome')
    return render(request, 'listar_orcamentos.html', {'orcamentos': orcamentos})

def processar_dentes(request):
    try:
        dentes_com_circulo = json.loads(request.POST.get('dentes_com_circulo', '[]'))
    except json.JSONDecodeError:
        dentes_com_circulo = []

    try:
        dentes_com_risco = json.loads(request.POST.get('dentes_com_risco', '[]'))
    except json.JSONDecodeError:
        dentes_com_risco = []

    try:
        dentes_com_circulo_nao_preenchido = json.loads(request.POST.get('dentes_com_circulo_nao_preenchido', '[]'))
    except json.JSONDecodeError:
        dentes_com_circulo_nao_preenchido = []

    try:
        dentes_com_x = json.loads(request.POST.get('dentes_com_x', '[]'))
    except json.JSONDecodeError:
        dentes_com_x = []

    return dentes_com_circulo, dentes_com_risco, dentes_com_circulo_nao_preenchido, dentes_com_x

def processar_procedimentos(request):
    procedimentos = []

    for key in request.POST:
        if key.startswith('nome-'):
            procedimento_id = key.split('-')[1]

            try:
                nome = request.POST.get(f'nome-{procedimento_id}').strip()
                preco = float(request.POST.get(f'preco-{procedimento_id}', 0) or 0)
                data_criacao_str = request.POST.get(f'data-criacao-{procedimento_id}')
                data_finalizado_str = request.POST.get(f'data-finalizado-{procedimento_id}')
                finalizado = request.POST.get(f'finalizado-{procedimento_id}') == 'on'

                data_criacao = datetime.strptime(data_criacao_str, '%Y-%m-%d').date() if data_criacao_str else datetime.today().date()
                data_finalizado = datetime.strptime(data_finalizado_str, '%Y-%m-%d').date() if data_finalizado_str else None

                procedimento = Procedimento.objects.create(
                    nome=nome,
                    preco=preco,
                    data_criacao=data_criacao,
                    data_finalizado=data_finalizado,
                    finalizado=finalizado
                )
                procedimentos.append(procedimento)

            except Exception as e:
                print(f"Erro ao processar procedimento: {e}")

    return procedimentos

@login_required(login_url="/auth/login")
def editar_orcamento(request, id):
    orcamento = get_object_or_404(Orcamento, id=id)
    clientes = Cliente.objects.all().order_by('nome')

    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            cliente = get_object_or_404(Cliente, id=cliente_id)

            dentes_com_circulo, dentes_com_risco, dentes_com_circulo_nao_preenchido, dentes_com_x = processar_dentes(request)
            procedimentos = processar_procedimentos(request)

            orcamento.cliente = cliente
            orcamento.anaminesia = request.POST.get('anaminesia') == 'on'
            orcamento.dentes_com_circulo = dentes_com_circulo
            orcamento.dentes_com_risco = dentes_com_risco
            orcamento.dentes_com_circulo_nao_preenchido = dentes_com_circulo_nao_preenchido
            orcamento.dentes_com_x = dentes_com_x
            orcamento.preco = float(request.POST.get('preco_total', 0) or 0)
            orcamento.pago = float(request.POST.get('pago', 0) or 0)
            orcamento.datas = json.loads(request.POST.get('datas', '[]'))
            orcamento.procedimentos.set(procedimentos)
            orcamento.save()

            return redirect('listar_orcamentos')

        except Exception as e:
            print(f"Erro ao editar orçamento: {e}")

    return render(request, 'cadastrar_orcamento.html', {
        'orcamento': orcamento,
        'clientes': clientes,
        'dentes': range(1, 65),
    })


@login_required(login_url="/auth/login")
def cadastrar_orcamento(request):
    clientes = Cliente.objects.filter(orcamentos__isnull=True).order_by('nome')

    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            cliente = get_object_or_404(Cliente, id=cliente_id)

            dentes_com_circulo, dentes_com_risco, dentes_com_circulo_nao_preenchido, dentes_com_x = processar_dentes(request)
            procedimentos = processar_procedimentos(request)

            orcamento = Orcamento.objects.create(
                cliente=cliente,
                anaminesia=request.POST.get('anaminesia') == 'on',
                dentes_com_circulo=dentes_com_circulo,
                dentes_com_risco=dentes_com_risco,
                dentes_com_circulo_nao_preenchido=dentes_com_circulo_nao_preenchido,
                dentes_com_x=dentes_com_x,
                preco=float(request.POST.get('preco_total', 0) or 0),
                pago=float(request.POST.get('pago', 0) or 0),
                datas=json.loads(request.POST.get('datas', '[]')),
            )
            orcamento.procedimentos.set(procedimentos)

            return redirect('listar_orcamentos')

        except Exception as e:
            print(f"Erro ao cadastrar orçamento: {e}")

    return render(request, 'cadastrar_orcamento.html', {
        'clientes': clientes,
        'dentes': range(1, 65),
    })

@login_required(login_url="/auth/login")
def excluir_orcamento(request, id):
    orcamento = get_object_or_404(Orcamento, id=id)
    if request.method == "POST":
        orcamento.delete()
        return redirect('listar_orcamentos')    

@login_required(login_url="/auth/login")
def agenda(request):
    clientes = Cliente.objects.prefetch_related('orcamentos').order_by('nome')

    # Monta um dicionário: {cliente_id: orcamento_id ou None}
    orcamentos = {
        cliente.id: cliente.orcamentos.id if hasattr(cliente, 'orcamentos') and cliente.orcamentos else None
        for cliente in clientes
    }

    context = {
        'clientes': clientes,
        'orcamentos': orcamentos,
    }
    return render(request, 'agenda.html', context)

@login_required(login_url="/auth/login")
def clientes(request):
    clientes = Cliente.objects.all().order_by('nome')
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required(login_url="/auth/login")
def cadastrar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        Cliente.objects.create(nome=nome, telefone=telefone, cpf=cpf)
        return redirect('listar_clientes')

@login_required(login_url="/auth/login")
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nome = request.POST.get('nome')
        cliente.telefone = request.POST.get('telefone')
        cliente.cpf = request.POST.get('cpf')
        cliente.save()
        return redirect('listar_clientes')

@login_required(login_url="/auth/login")
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')

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
                "protetico": evento.protetico,
                # "cliente":  evento.cliente
            } for evento in eventos
        ]
        
        dentistas_json.append({
            "id": dentista.id,
            "nome": dentista.nome,
            "eventos": eventos_serializados,
        })
 
    return JsonResponse(dentistas_json, safe=False)

@csrf_exempt
@login_required(login_url="/auth/login")
def cadastrar_dentista(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        Dentista.objects.create(nome=nome)
        return redirect('agenda')

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
            "protetico": evento.protetico,
            "cliente": evento.cliente.id if evento.cliente else None,
            "dentista": evento.dentista.nome if evento.dentista else None,
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
            data_inicio = data.get('data_inicio')
            data_fim = data.get('data_fim')
            dentista_id = data.get('dentista')
            cliente_id = data.get('cliente')  # Novo campo
            protetico = data.get('protetico')

            dentista = Dentista.objects.get(id=dentista_id) if dentista_id else None
            cliente = Cliente.objects.get(id=cliente_id) if cliente_id else None

            if evento_id:
                evento = Evento.objects.get(id=evento_id)
                evento.titulo = titulo
                evento.data_inicio = data_inicio
                evento.data_fim = data_fim
                evento.dentista = dentista
                evento.cliente = cliente
                evento.protetico = protetico
                evento.save()
            else:
                Evento.objects.create(
                    titulo=titulo,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    dentista=dentista,
                    cliente=cliente,
                    protetico=protetico
                )

            return JsonResponse({"status": "success"})

        except (Dentista.DoesNotExist, Cliente.DoesNotExist):
            return JsonResponse({"status": "error", "message": "Dentista ou Cliente não encontrado!"}, status=400)

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
