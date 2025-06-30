from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linked_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    link_precedence = Column(String, nullable=False, default="primary")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
