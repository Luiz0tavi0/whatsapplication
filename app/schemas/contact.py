from pydantic import BaseModel


class ContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    lid: str | None = None

    model_config = {'from_attributes': True}
