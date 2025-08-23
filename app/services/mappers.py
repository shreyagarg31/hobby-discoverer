from app.models.user import User, DBUser
from typing import Optional

def dbuser_to_user(db_user: DBUser) -> User:
    """
    Maps internal DBUser (includes hashed password) to public User model.
    """
    try:
        return User(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            profile=db_user.profile,
            created_at=db_user.created_at
        )
    except Exception as e:
        print("Error mapping to User: ", str(e))
        return None


def safe_dbuser_to_user(db_user: Optional[DBUser]) -> Optional[User]:
    if db_user is None:
        return None
    user = dbuser_to_user(db_user)
    return user
