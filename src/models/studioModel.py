from sqlalchemy import Boolean, Column, Integer, String

from ..db.database import Base


class Studio(Base):
    __tablename__ = "studio"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(20))
    name = Column(String(50))
    address = Column(String(100))
    contact = Column(String(50))
    latitude = Column(String(20))  # 위도
    longitude = Column(String(20))  # 경도
    is_opened = Column(Boolean, default=True)
