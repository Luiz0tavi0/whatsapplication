# wa-notifier

Lê contatos do Supabase e envia `"Olá, <nome> tudo bem com você?"` via WhatsApp, com fallback automático (Z-API → WireWeb).

## Setup da tabela
```sql
create table contacts (
    id bigint generated always as identity primary key,
    name text not null,
    phone text not null,
    lid text unique,
    created_at timestamptz default now() not null,
    updated_at timestamptz default now() not null,
    unique (phone, lid)
);

create table dispatches (
    id bigint generated always as identity primary key,
    idempotency_key text unique not null,
    message_hash text not null,
    provider text not null,
    provider_message_id text,
    phone text not null,
    lid text,
    status text not null check (status in ('pending','sent','received','read','failed')),
    created_at timestamptz default now() not null,
    updated_at timestamptz default now() not null
);

create index ix_dispatches_provider_message_id on dispatches (provider_message_id);
```
## Variáveis de ambiente

```bash
cp .env.example .env
```

| Variável | Obrigatória | Descrição |
|---|---|---|
| `DATABASE_URL` | ✅ | Supabase → Settings → Database → **Transaction pooler** → trocar `postgresql://` por `postgresql+asyncpg://` |
| `ZAPI_INSTANCE` | ✅ | ID da instância Z-API |
| `ZAPI_BASE_URL` | ✅ | `https://api.z-api.io/` |
| `ZAPI_TOKEN` | ✅ | Token da instância Z-API |
| `WIREWEB_BASE_URL` | ⬜ | Ex: `https://api.wireweb.co.in` |
| `WIREWEB_API_KEY` | ⬜ | Chave de API WireWeb |
| `WIREWEB_SESSION_ID` | ⬜ | ID da sessão WireWeb |
| `WIREWEB_WEBHOOK_TOKEN` | ⬜ | Token secreto para validar webhooks WireWeb |
| `PROVIDERS_ORDER` | ⬜ | Default: `["zapi","wireweb"]` |

> `DATABASE_URL` deve usar o **Transaction pooler** (porta `6543`) — a conexão direta do Supabase é IPv6-only.

## Como rodar

```bash
uv sync
uv run alembic upgrade head
uv run python -m app.main
```

Envia para até 3 contatos. Tenta Z-API primeiro; em falha aplica retry com backoff e cai para WireWeb.

## Webhooks de status (opcional)

```bash
uv run fastapi dev server.py
ngrok http 8000
```

| Provedor | URL |
|---|---|
| Z-API | `https://<ngrok>/webhooks/zapi/status?token=<ZAPI_TOKEN>` |
| WireWeb | `https://<ngrok>/webhooks/wireweb/status?token=<WIREWEB_WEBHOOK_TOKEN>` |

Status evolui via webhook: `pending` → `sent` → `received` → `read` / `failed`.
