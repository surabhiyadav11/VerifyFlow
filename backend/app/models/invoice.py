import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Index, Integer, Numeric, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"
    __table_args__ = (Index("ix_invoices_number_vendor_gstin", "invoice_number", "vendor_gstin"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    check_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("checks.id", ondelete="CASCADE"),
        nullable=False,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    invoice_number: Mapped[str | None] = mapped_column(Text, nullable=True)
    invoice_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    vendor_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    vendor_gstin: Mapped[str | None] = mapped_column(Text, nullable=True)
    vendor_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    buyer_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    buyer_gstin: Mapped[str | None] = mapped_column(Text, nullable=True)
    place_of_supply: Mapped[str | None] = mapped_column(Text, nullable=True)
    currency: Mapped[str] = mapped_column(Text, nullable=False, default="INR")
    subtotal: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    cgst_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    sgst_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    igst_amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    total_tax: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    total: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)

    check: Mapped["Check"] = relationship("Check", back_populates="invoices")
    document: Mapped["Document"] = relationship("Document", back_populates="invoice")
    line_items: Mapped[list["InvoiceLineItem"]] = relationship(
        "InvoiceLineItem",
        back_populates="invoice",
        cascade="all, delete-orphan",
        order_by="InvoiceLineItem.position",
    )


class InvoiceLineItem(Base, TimestampMixin):
    __tablename__ = "invoice_line_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    hsn_sac: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity: Mapped[Decimal | None] = mapped_column(Numeric(14, 3), nullable=True)
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    tax_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="line_items")

