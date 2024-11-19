document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    function ajustarFusoHorario(date) {
        // Obtém o deslocamento do fuso horário em milissegundos
        const offset = date.getTimezoneOffset() * 60000;
        // Ajusta o tempo e retorna no formato ISO sem alterar o dia
        return new Date(date.getTime() - offset).toISOString().slice(0, 16);
    }

    var calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
        },
        buttonText: {
            today: 'Hoje',
            month: 'Mês',
            week: 'Semana',
            day: 'Dia',
            list: 'Lista'
        },
        initialDate: '2023-01-12',
        navLinks: true,
        businessHours: true,
        editable: true,
        selectable: true,
        initialView: 'timeGridWeek',
        initialDate: new Date().toISOString().slice(0, 10), // A data de hoje no formato yyyy-mm-dd
        locale: 'pt-br',

        events: function (info, successCallback, failureCallback) {
            const dentistaId = new URLSearchParams(window.location.search).get('dentista_id');
            const url = dentistaId ? `/events/${dentistaId}/` : '/events/';

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    successCallback(data); // Passa os eventos para o calendário
                })
                .catch(error => {
                    failureCallback(error);
                    console.error('Erro ao carregar eventos:', error);
                });
        },

        dateClick: function (info) {
            const now = new Date();

            let selectedDate;
            if (info.dateStr.length > 10) {
                selectedDate = new Date(info.dateStr);
            } else {
                selectedDate = new Date(info.dateStr + "T00:00:00");
                selectedDate.setHours(now.getHours(), now.getMinutes(), 0, 0);
            }

            const startDateTime = ajustarFusoHorario(selectedDate);
            const endDateTime = ajustarFusoHorario(new Date(selectedDate.getTime() + 30 * 60000)); // +30 minutos

            // Preencher os campos do modal
            document.getElementById("eventStart").value = startDateTime;
            document.getElementById("eventEnd").value = endDateTime;
            document.getElementById("eventTitle").value = '';
            document.getElementById("eventDescription").value = '';
            document.getElementById("eventId").value = '';

            // Altera o título e exibe apenas o botão Salvar
            document.getElementById("eventModalLabel").textContent = 'Cadastrar Evento';
            document.getElementById("deleteEvent").style.display = 'none'; // Oculta o botão excluir

            const eventModal = new bootstrap.Modal(document.getElementById("eventModal"));
            eventModal.show();
        },

        // Ativado ao clicar em um evento
        eventClick: function (info) {
            const evento = info.event;

            // Preencher os campos do modal com os dados do evento, ajustando os horários
            document.getElementById("eventTitle").value = evento.title;
            document.getElementById("eventDescription").value = evento.extendedProps.description || '';
            document.getElementById("eventStart").value = ajustarFusoHorario(evento.start);
            document.getElementById("eventEnd").value = evento.end ? ajustarFusoHorario(evento.end) : '';
            document.getElementById("eventId").value = evento.id;

            // Altera o título para Evento e exibe o botão Excluir
            document.getElementById("eventModalLabel").textContent = 'Evento';
            document.getElementById("deleteEvent").style.display = 'inline-block';

            const eventModal = new bootstrap.Modal(document.getElementById("eventModal"));
            eventModal.show();
        },

        eventDrop: function (info) {
            let evento = info.event;
            const duracao = evento.end ? evento.end.getTime() - evento.start.getTime() : 3600000; // 1 hora
            const novaDataInicio = evento.start.toISOString();
            const novaDataFim = new Date(evento.start.getTime() + duracao).toISOString();

            fetch('/atualizar_evento/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({
                    id: evento.id,
                    data_inicio: novaDataInicio,
                    data_fim: novaDataFim
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        // alert("Evento atualizado com sucesso!");
                    } else {
                        alert("Erro ao atualizar o evento.");
                        info.revert();
                    }
                })
                .catch(() => {
                    alert("Erro ao comunicar com o servidor.");
                    info.revert();
                });
        },

        eventResize: function (info) {
            let evento = info.event;
            const novaDataInicio = evento.start.toISOString();
            const novaDataFim = evento.end.toISOString();

            fetch('/atualizar_evento/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({
                    id: evento.id,
                    data_inicio: novaDataInicio,
                    data_fim: novaDataFim
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        // alert("Evento atualizado com sucesso!");
                    } else {
                        alert("Erro ao atualizar o evento.");
                        info.revert();
                    }
                })
                .catch(() => {
                    alert("Erro ao comunicar com o servidor.");
                    info.revert();
                });
        }
    });

    document.getElementById("saveEvent").addEventListener("click", function () {
        const id = document.getElementById("eventId").value;
        const titulo = document.getElementById("eventTitle").value;
        const descricao = document.getElementById("eventDescription").value;
        const inicio = document.getElementById("eventStart").value;  // Pegue a data selecionada no modal
        const fim = document.getElementById("eventEnd").value;
        const dentistaId = new URLSearchParams(window.location.search).get('dentista_id');

        // Passar essas verificações para o modal
        if (!titulo || !inicio) {
            alert("Título e início são obrigatórios!");
            return;
        }

        if (!dentistaId) {
            alert("Selecione um dentista antes de cadastrar o evento!");
            return;
        }

        const eventoData = {
            titulo: titulo,
            descricao: descricao,
            data_inicio: new Date(inicio).toISOString(),
            data_fim: fim ? new Date(fim).toISOString() : null,
            dentista: dentistaId
        };

        if (id) {
            // Atualizando evento
            eventoData.id = id;
        }

        fetch('/cadastrar_evento/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify(eventoData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    calendar.refetchEvents();
                    const eventModal = bootstrap.Modal.getInstance(document.getElementById("eventModal"));
                    eventModal.hide();
                } else {
                    alert("Erro ao salvar o evento: " + data.message);
                }
            })
            .catch(() => {
                alert("Erro ao comunicar com o servidor.");
            });
    });

    document.getElementById("deleteEvent").addEventListener("click", function () {
        const id = document.getElementById("eventId").value;

        fetch(`/deletar_evento/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    const eventModal = bootstrap.Modal.getInstance(document.getElementById("eventModal"));
                    eventModal.hide();
                    calendar.refetchEvents();
                } else {
                    alert("Erro ao deletar o evento: " + data.message);
                }
            })
            .catch(() => {
                alert("Erro ao comunicar com o servidor.");
            });
    });

    document.addEventListener('dentistaSelecionado', function (event) {
        calendar.refetchEvents();
    });

    calendar.render();
});