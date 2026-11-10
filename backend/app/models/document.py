import enum
import uuid
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Numeric, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class DocumentLabel(str, enum.Enum):
    invoice = "invoice"
    pan = "pan"
    aadhaar = "aadhaar"
    address_proof = "address_proof"
    passport = "passport"
    driving_licence = "driving_licence"
    selfie = "selfie"


class ExtractionStatus(str, enum.Enum):
    pending = "pending"
    done = "done"
    failed = "failed"


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    check_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("checks.id", ondelete="CASCADE"),
        nullable=False,
    )
    label: Mapped[DocumentLabel] = mapped_column(
        Enum(DocumentLabel, name="document_label_enum"),
        nullable=False,
    )
    original_filename: Mapped[str] = mapped_column(Text, nullable=False)
    mime_type: Mapped[str] = mapped_column(Text, nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    extraction_status: Mapped[ExtractionStatus] = mapped_column(
        Enum(ExtractionStatus, name="extraction_status_enum"),
        nullable=False,
        default=ExtractionStatus.pending,
    )
    extraction_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    ocr_engine: Mapped[str] = mapped_column(Text, nullable=False, default="tesseract")
    ocr_confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    readability: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    fields: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    field_meta: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    id_format_valid: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    id_hash: Mapped[str | None] = mapped_column(Text, nullable=True)

    check: Mapped["Check"] = relationship("Check", back_populates="documents")
    invoice: Mapped["Invoice | None"] = relationship(
        "Invoice", back_populates="document", uselist=False, cascade="all, delete-orphan"
    )
    issues: Mapped[list["Issue"]] = relationship("Issue", back_populates="document")

