function carregarDentistas() {
    fetch('/dentistas/')
        .then(response => response.json())
        .then(dentistas => {
            const dentistasList = document.getElementById('dentistas-list');
            dentistasList.innerHTML = '';

            if (dentistas.length > 0) {
                dentistas.forEach(dentista => {
                    const li = document.createElement('li');
                    li.classList.add('list-group-item');
                    li.textContent = dentista.nome;
                    li.setAttribute('data-id', dentista.id);
                    dentistasList.appendChild(li);
                });

                selecionarDentista(dentistas[0].id);
            } else {
                const li = document.createElement('li');
                li.classList.add('list-group-item');
                li.textContent = 'Nenhum dentista cadastrado.';
                dentistasList.appendChild(li);
            }
        })
        .catch(error => {
            console.error('Erro ao carregar dentistas:', error);
        });
}

function selecionarDentista(dentistaId) {
    const dentistasList = document.getElementById('dentistas-list');
    const primeiroDentista = dentistasList.querySelector(`[data-id="${dentistaId}"]`);

    if (primeiroDentista) {
        // Remove a classe 'active' dos outros itens
        document.querySelectorAll('#dentistas-list .list-group-item').forEach(function (item) {
            item.classList.remove('active');
        });

        // Marca o dentista como 'ativo'
        primeiroDentista.classList.add('active');

        // Atualiza a URL sem recarregar a página
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('dentista_id', dentistaId); // Adiciona ou atualiza o parâmetro dentista_id
        window.history.pushState({}, '', currentUrl); // Atualiza a URL no navegador

        // Dispara o evento 'dentistaSelecionado' para a agenda
        const dentistaSelecionadoEvent = new CustomEvent('dentistaSelecionado', {
            detail: { dentistaId: dentistaId }
        });
        document.dispatchEvent(dentistaSelecionadoEvent);
    }
}

document.getElementById('dentistas-list').addEventListener('click', function (event) {
    if (event.target && event.target.matches('li.list-group-item')) {
        const dentistaId = event.target.getAttribute('data-id');
        selecionarDentista(dentistaId);  // Chama a função para selecionar o dentista clicado
    }
});

document.addEventListener('DOMContentLoaded', carregarDentistas);