from app.models.user import UserCreate, UserLogin, User, UserProfile, DBUser
from app.utils.security import hash_password, verify_password
from datetime import datetime
from bson import ObjectId
from app.config.settings import MongoManager

async def get_user_by_email(email: str):
    users_collection = MongoManager.get_collection("users")
    user = await users_collection.find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
        return DBUser(**user)
    return None

async def create_user_in_db(user: UserCreate):
    users_collection = MongoManager.get_collection("users")
    hashed_pw = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_pw
    user_dict.pop("password")
    user_dict["created_at"] = datetime.utcnow()
    result = await users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    # Return DBUser for internal use, User for API response
    return User(
        id=user_dict["id"],
        email=user_dict["email"],
        name=user_dict["name"],
        profile=UserProfile(**user_dict["profile"]),
        created_at=user_dict["created_at"]
    )

async def verify_user_credentials(email: str, password: str):
    users_collection = MongoManager.get_collection("users")
    user = await users_collection.find_one({"email": email})
    if user and verify_password(password, user["hashed_password"]):
        user["id"] = str(user["_id"])
        return DBUser(**user)
    return None

async def get_user_by_id(user_id: str):
    users_collection = MongoManager.get_collection("users")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        return DBUser(**user)
    return None

async def update_user_profile_in_db(user_id: str, profile: UserProfile):
    users_collection = MongoManager.get_collection("users")
    profile_dict = profile.dict()
    profile_dict["updated_at"] = datetime.utcnow()
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"profile": profile_dict}}
    )
    if result.modified_count == 1:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        return UserProfile(**user["profile"])
    return None