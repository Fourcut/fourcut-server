from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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

    favorites = relationship("Favorite")
    histories = relationship("History")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50))
    name = Column(String(20))
    avatar = Column(String(500))
    is_member = Column(Boolean, default=True)

    favorites = relationship("Favorite")
    user_histories = relationship("UserHistory")


class Favorite(Base):
    __tablename__ = "favorite"
    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("studio.id"))
    user_id = Column(Integer, ForeignKey("user.id"))


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))  # 추가
    studio_id = Column(Integer, ForeignKey("studio.id"))

    user_histories = relationship("UserHistory")
    files = relationship("File")


class UserHistory(Base):
    __tablename__ = "user_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    history_id = Column(Integer, ForeignKey("history.id"))


class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True, index=True)
    history_id = Column(Integer, ForeignKey("history.id"))
    url = Column(String(500))
