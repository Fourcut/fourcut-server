from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
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

    favorites = relationship(
        "Favorite",
        back_populates="studio",
    )
    histories = relationship(
        "History",
        back_populates="studio",
    )


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), unique=True)
    email = Column(String(50))
    name = Column(String(20))
    avatar = Column(String(500))
    is_member = Column(Boolean, default=True)

    favorites = relationship("Favorite", back_populates="user")
    user_histories = relationship("UserHistory", back_populates="user")

    def __init__(self, client_id, email, name, avatar, is_member):
        self.client_id = client_id
        self.email = email
        self.name = name
        self.avatar = avatar
        self.is_member = is_member


class Favorite(Base):
    __tablename__ = "favorite"
    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("studio.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    studio = relationship(
        "Studio",
        back_populates="favorites",
    )
    user = relationship(
        "User",
        back_populates="favorites",
    )

    def __init__(self, studio_id, user_id):
        self.studio_id = studio_id
        self.user_id = user_id


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))  # 추가
    studio_id = Column(Integer, ForeignKey("studio.id"))
    history_date = Column(Date)

    studio = relationship(
        "Studio",
        back_populates="histories",
    )
    user_histories = relationship(
        "UserHistory",
        back_populates="history",
    )
    files = relationship(
        "File",
        back_populates="history",
    )

    def __init__(self, studio_id, title, history_date):
        self.title = title
        self.studio_id = studio_id
        self.history_date = history_date


class UserHistory(Base):
    __tablename__ = "user_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    history_id = Column(Integer, ForeignKey("history.id"))

    history = relationship(
        "History",
        back_populates="user_histories",
    )
    user = relationship(
        "User",
        back_populates="user_histories",
    )

    def __init__(self, user_id, history_id):
        self.user_id = user_id
        self.history_id = history_id


class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True, index=True)
    history_id = Column(Integer, ForeignKey("history.id"))
    url = Column(String(500))

    history = relationship(
        "History",
        back_populates="files",
    )

    def __init__(self, history_id, url):
        self.history_id = history_id
        self.url = url
