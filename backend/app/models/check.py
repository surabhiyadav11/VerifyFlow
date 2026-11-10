import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class DocType(str, enum.Enum):
    invoice = "invoice"
    kyc = "kyc"


class CheckStatus(str, enum.Enum):
    draft = "draft"
    extracted = "extracted"
    validated = "validated"


class OverallStatus(str, enum.Enum):
    pass_ = "pass"
    needs_review = "needs_review"
    fail = "fail"


class Check(Base, TimestampMixin):
    __tablename__ = "checks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_type: Mapped[DocType] = mapped_column(Enum(DocType, name="doc_type_enum"), nullable=False)
    status: Mapped[CheckStatus] = mapped_column(
        Enum(CheckStatus, name="check_status_enum"),
        nullable=False,
        default=CheckStatus.draft,
    )
    overall_status: Mapped[OverallStatus | None] = mapped_column(
        Enum(
            OverallStatus,
            name="overall_status_enum",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=True,
    )
    report_stale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    documents: Mapped[list["Document"]] = relationship(
        "Document", back_populates="check", cascade="all, delete-orphan"
    )
    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice", back_populates="check", cascade="all, delete-orphan"
    )
    issues: Mapped[list["Issue"]] = relationship(
        "Issue", back_populates="check", cascade="all, delete-orphan"
    )

