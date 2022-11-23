from .db.database import SessionLocal
from .models.models import Favorite, File, History, User, UserHistory

session = SessionLocal()

user1 = User(email="u1@gmail.com", name="u1", avatar=None, is_member=None)
favorite1 = Favorite(studio_id=1, user_id=None)
user1.favorites = [favorite1]

history1 = History(studio_id=1, title="history1")
file1 = File(url="file1url", history_id=None)
history1.files = [file1]
session.add(user1)
session.add(favorite1)
session.add(history1)
session.add(file1)

session.flush()

session.refresh(user1)
session.refresh(history1)

user_history1 = UserHistory(user_id=user1.id, history_id=history1.id)

session.add(user_history1)
session.flush()
session.refresh(user_history1)

# session.delete(user1)  # 다른 row 가 참조하고 있어서 삭제안됨
session.delete(user_history1)

session.commit()
session.close()