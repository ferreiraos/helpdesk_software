# helpdesk_software

Sistema de gerenciamento de chamados simples, local e organizado.

## Estrutura sugerida

- `backend/`
  - `database.py` → conexão SQLite e sessão
  - `models.py` → entidades Chamado, Mensagem, Feedback e Histórico
  - `schemas.py` → contratos Pydantic para a API
  - `services.py` → regras de negócio e manipulação de dados
  - `routes.py` → endpoints REST para frontend
  - `main.py` → configuração FastAPI e rota principal
- `front/`
  - `templates/index.html` → interface de uma única página
  - `static/` → `style.css` e `app.js`
- `helpdesk.db` → banco de dados SQLite local
- `main.py` → comando simples para rodar o app

## Como executar

```bash
python main.py
```

ou

```bash
uvicorn main:app --reload
```

Em seguida abra:

```text
http://127.0.0.1:8000
```

## Funcionalidades

- Criar e listar chamados
- Visualizar detalhes do chamado
- Atualizar status (aberto, em andamento, resolvido)
- Histórico de mudanças de status
- Mensagens do tipo chat dentro do chamado
- Feedback com nota e comentário após resolução
