from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base

def utcnow(): return datetime.utcnow()

class Play(Base):
    __tablename__ = "plays"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    persona: Mapped[str] = mapped_column(String(80), index=True, default="general")
    objection: Mapped[str] = mapped_column(String(200), index=True)
    talk_track: Mapped[str] = mapped_column(Text)
    proof: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
