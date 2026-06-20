
from sqlalchemy import BigInteger, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from app.models import table_registry
from app.models.mixins import DateMixin


@mapped_as_dataclass(table_registry)
class Dispatch(DateMixin):
    __tablename__ = 'dispatches'
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','sent','received','read','failed')",
            name='ck_dispatch_status_valid',
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    idempotency_key: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    message_hash: Mapped[str] = mapped_column(String, nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    provider_message_id: Mapped[str | None] = mapped_column(
        String, nullable=True, index=True
    )
    phone: Mapped[str] = mapped_column(String, nullable=False)
    lid: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default='pending')
