# Consultório de Dentista

Este é um projeto desenvolvido em Django para um consultório de dentista. O sistema permite o gerenciamento de eventos, agendamentos e informações relacionadas aos pacientes e dentistas. O projeto utiliza **Bootstrap** para a interface e **FullCalendar.io** para exibir os agendamentos de forma interativa.

## Funcionalidades

- **Cadastro de clientes**: Permite registrar informações dos clientes.
- **Gerenciamento de agendamentos**: Utiliza o FullCalendar.io para visualizar e gerenciar os horários disponíveis para os dentistas.
- **Interface responsiva**: A interface do usuário é responsiva e foi construída utilizando o framework Bootstrap.
- **Autenticação**: Sistema de login e autenticação de usuários para diferentes permissões (administradores, dentistas).

## Tecnologias utilizadas

- **Django**: Framework web utilizado para o desenvolvimento do backend.
- **Bootstrap**: Framework front-end utilizado para a construção da interface responsiva.
- **FullCalendar.io**: Biblioteca JavaScript para a exibição de eventos (agendamentos) em formato de calendário.
- **SQLite**: Banco de dados utilizado para armazenar os dados.

## Como rodar o projeto

Siga os passos abaixo para rodar o projeto localmente.

### Pré-requisitos

- Python 3.x
- Django
- Node.js (para o FullCalendar)

### Passo a passo

1. Clone o repositório:

    ```bash
    git clone https://github.com/RamalhoJP/consultorio-dias.git 
    ```

2. Navegue até o diretório do projeto:

    ```bash
    cd consultorio-dias
    ```

3. Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4. Execute as migrações para criar o banco de dados:

    ```bash
    python manage.py migrate
    ```

5. Execute o servidor de desenvolvimento:

    ```bash
    python manage.py runserver
    ```

O projeto estará acessível em [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
