import enum
import uuid
from typing import Any

from sqlalchemy import Enum, ForeignKey, Text, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class IssueSeverity(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Issue(Base, TimestampMixin):
    __tablename__ = "issues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    check_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("checks.id", ondelete="CASCADE"),
        nullable=False,
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=True,
    )
    rule_code: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[IssueSeverity] = mapped_column(
        Enum(IssueSeverity, name="issue_severity_enum"),
        nullable=False,
    )
    field: Mapped[str | None] = mapped_column(Text, nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_fix: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    check: Mapped["Check"] = relationship("Check", back_populates="issues")
    document: Mapped["Document | None"] = relationship("Document", back_populates="issues")

