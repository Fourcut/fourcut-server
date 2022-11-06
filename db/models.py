from sqlalchemy import Column, Integer, String

from .database import Base


class Studios(Base):
    __tablename__ = "studios"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(20))
    name = Column(String(50))
    address = Column(String(100))
    contact = Column(String(50))
    zip_code = Column(Integer)
