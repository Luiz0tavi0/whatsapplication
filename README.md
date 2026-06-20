# WA Notifier

Lê contatos do Supabase e envia mensagem personalizada via WhatsApp, com fallback automático entre provedores (Z-API → WireWeb).

## Setup da tabela (Supabase)

```sql
create table contacts (
    id bigint generated always as identity primary key,
    nome text not null,
    telefone text not null,
    lid text
);
```

`telefone` no formato DDI+DDD+número, ex: `5511999999999`.
`lid` é opcional, preenchido depois (usado só pela Z-API quando disponível).

Rodar migrations (cria também a tabela `dispatches`):

```bash
uv run alembic upgrade head
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | connection string do Postgres (Supabase → Settings → Database, trocar `postgresql://` por `postgresql+asyncpg://`) |
| `ZAPI_INSTANCE` / `ZAPI_TOKEN` / `ZAPI_CLIENT_TOKEN` | credenciais da Z-API |
| `WIREWEB_BASE_URL` / `WIREWEB_API_KEY` / `WIREWEB_SESSION_ID` | credenciais do WireWeb (fallback) |
| `PROVIDERS_ORDER` | ordem de tentativa, ex: `["zapi","wireweb"]` |

## Como rodar

```bash
uv sync
cp .env.example .env   # preencher
uv run alembic upgrade head
uv run python -m app.main
```

Envia "Olá, `<nome>` tudo bem com você?" para até 3 contatos cadastrados. Se o Z-API falhar, tenta automaticamente o WireWeb.

## Dev

```bash
uv run ruff check .
```
