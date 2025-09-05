from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Boolean, DateTime, func
from datetime import datetime

class SoftDeleteMixin(SQLModel):
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
    is_deleted: bool = Field(
        default=False,
        sa_column=Column(Boolean, nullable=False)
    )
