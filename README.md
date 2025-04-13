# Meus Podcasts - Backend

<div align="center">
    <img src="https://img.shields.io/badge/python-3.12%2B-yellow" alt="Python Version">
</div>

<div align="center">
  <h3 align="center">Meus Podcasts</h3>
  <p align="center">
    Uma plataforma para gerenciar e explorar seus podcasts favoritos.
    <br />
    <a href="https://github.com/gav1ao/my-podcasts-backend"><strong>Explore a documentação »</strong></a>
    <br />
    <br />
    <a href="https://github.com/gav1ao/my-podcasts-backend/issues">Reportar Bug</a>
    ·
    <a href="https://github.com/gav1ao/my-podcasts-backend/issues">Solicitar Feature</a>
  </p>
</div>

---

## Sobre o Projeto

O **Meus Podcasts (Backend)** é uma aplicação backend desenvolvida em Python que fornece uma REST API robusta para gerenciar podcasts. A API permite aos usuários explorar, favoritar e organizar seus podcasts favoritos, além de oferecer suporte para autenticação, cadastro de usuários e importação de podcasts via RSS Feed.

---

## Tecnologias Utilizadas

- [Python 3.12+](https://www.python.org/doc/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)

---

## Como Começar

### Pré-requisitos

- Python 3.12+ instalado em sua máquina.
- `pip` (Python Package Installer) atualizado.
- Banco de dados configurado (ex.: PostgreSQL, MySQL ou SQLite).
- `alembic` instalado para gerenciar migrações.

### Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/gav1ao/my-podcasts-backend.git
   ```

2. Navegue até o diretório do projeto:

   ```sh
   cd my-podcasts-backend
   ```

3. Crie e ative um ambiente virtual:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

5. Configure as variáveis de ambiente:

   - Faça uma cópia do arquivo `.env.sample` e renomeie-o para `.env`;
   - Configure as variáveis necessárias (ex.: chaves secretas, duração de tokens).

6. Execute as migrações do banco de dados:
   ```sh
   alembic upgrade head
   ```

## Uso

1. Inicie a aplicação a partir de um ambiente virtual com o seguinte comando:

   ```sh
   flask run --host 0.0.0.0 --port 8080
   ```

2. A API estará disponível em: [http://localhost:8080](http://localhost:8080).

3. Consulte a documentação da API (Swagger, RapiDoc ou Redoc)para detalhes sobre os endpoints e como utilizá-los em: [http://localhost:8080/openapi/](http://localhost:8080/openapi/).

## Desenvolvimento

Durante o desenvolvimento, recomenda-se executar a aplicação utilizando o parâmetro `--reload`, pois, a cada alteração no código, o servidor será reiniciado automaticamente.

```sh
flask run --host 0.0.0.0 --port 8080 --reload
```

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`).
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`).
4. Faça um push para a branch (`git push origin feature/NovaFeature`).
5. Abra um Pull Request.

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## Contato

Vítor Gavião - [@vigal_jan](https://x.com/vigal_jan) - vitor.gaviao@protonmail.com

Link do Projeto: [https://github.com/gav1ao/my-podcasts-backend](https://github.com/gav1ao/my-podcasts-backend)

Link do Frontend relacionado: [https://github.com/gav1ao/my-podcasts-frontend](https://github.com/gav1ao/my-podcasts-frontend)
