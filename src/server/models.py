from sqlalchemy import Column, Integer, String, DateTime, func
from src.server.database import Base
from datetime import datetime

class JSONData(Base):
    __tablename__ = "json_data"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 


# айди вроде как назначается на 1 больше чем максимальный айди в таблице (да)
