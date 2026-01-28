from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from .db import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(200), nullable=False, index=True)
    role = Column(String(200), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="applied", index=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
