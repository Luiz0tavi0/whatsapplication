from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from app.models import table_registry
from app.models.mixins import DateMixin


@mapped_as_dataclass(table_registry)
class Contact(DateMixin):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    lid: Mapped[str | None] = mapped_column(String, nullable=True)
