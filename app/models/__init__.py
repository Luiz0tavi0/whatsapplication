from sqlalchemy.orm import registry

table_registry = registry()
# from contact import Contact
from app.models.contact import Contact as Contact  # noqa: E402
from app.models.dispatch import Dispatch as Dispatch  # noqa: E402
