from typing import Optional

from pydantic import BaseModel


class BaseStatusPayload(BaseModel):
    messageId: str


class ZApiStatusPayload(BaseModel):
    instanceId: str
    type: str
    status: Optional[str] = None
    phone: Optional[str] = None
    messageId: Optional[str] = None
    ids: Optional[list[str]] = None


class WireWebStatusPayload(BaseStatusPayload):
    event: str
    sessionId: str
