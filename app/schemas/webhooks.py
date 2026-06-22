from pydantic import BaseModel


class BaseStatusPayload(BaseModel):
    messageId: str


class ZApiStatusPayload(BaseStatusPayload):
    instanceId: str
    status: str


class WireWebStatusPayload(BaseStatusPayload):
    event: str
    sessionId: str
