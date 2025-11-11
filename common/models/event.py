from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from common.models.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), index=True, nullable=False)
    deployment_id = Column(String(100), index=True)
    component_name = Column(String(100), index=True)
    status = Column(String(50))
    message = Column(String(500))
    payload = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
