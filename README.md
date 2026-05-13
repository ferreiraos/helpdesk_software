# Helpdesk Local

Sistema de helpdesk simples e funcional rodando localmente com Python, SQLite e frontend leve em HTML/CSS/JavaScript.

## Estrutura sugerida

- `backend/`
  - `main.py` - inicializa a aplicação FastAPI e serve a interface SPA
  - `database.py` - conexão SQLite e fábrica de sessões
  - `models.py` - modelos SQLAlchemy e relações de dados
  - `schemas.py` - definições Pydantic para entrada/saída de API
  - `routes.py` - endpoints REST organizados em API
  - `services/` - regras de negócio e operações de banco
- `front/`
  - `index.html` - interface de uma única página
  - `static/`
    - `app.js` - lógica de UI dinâmica sem reload completo
    - `style.css` - estilo simples e responsivo
- `helpdesk.db` - banco SQLite local
- `requirements.txt` - dependências do Python

## Funcionalidades

- Chamados
  - Criar chamado
  - Listar chamados
  - Visualizar detalhes
  - Atualizar status (aberto, em andamento, resolvido)
- Mensagens dentro do chamado
- Feedback após resolução
- Histórico de mudanças de status
- Interface em uma única tela

## Instalação e execução

1. Crie um ambiente virtual (recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicie a aplicação:

```bash
cd backend
python main.py
```

4. Abra no navegador:

```text
http://localhost:8000
```

## Observações

- O banco de dados é local, não há serviços externos.
- A interface funciona como um SPA com atualizações dinâmicas via JavaScript puro.
- A arquitetura separa endpoints, serviços e modelos para facilitar manutenção.

