from datetime import datetime

from pydantic import BaseModel


class DispatchResponse(BaseModel):
    id: int
    idempotency_key: str
    provider: str
    provider_message_id: str | None
    phone: str
    lid: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}


class SendMessageRequest(BaseModel):
    phone: str
    name: str
    lid: str | None = None


class SendMessageResponse(BaseModel):
    idempotency_key: str
    provider: str
    provider_message_id: str | None
    status: str
