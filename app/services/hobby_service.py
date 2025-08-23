from datetime import datetime
from typing import Optional
from app.models.hobby import HobbyPrompt
from app.models.user import User, DBUser 
from app.config.gen_ai_client import generate_hobby_suggestions
from app.config.settings import MongoManager
from app.services.mappers import safe_dbuser_to_user

def craft_prompt(user: User, extra_prompt: str) -> str:
    return (
        f"User Profile:\n"
        f"- Location: {user.profile.location}\n"
        f"- Time available per week: {user.profile.time_available} hours\n"
        f"- Prefers indoor: {user.profile.prefers_indoor}\n"
        f"- Social preference: {user.profile.social_preference}\n"
        f"- Interests: {', '.join(user.profile.interests)}\n\n"
        f"Additional input: {extra_prompt}\n\n"
        "As a creative lifestyle coach, suggest 3 unconventional, personalized hobby ideas "
        "that align with the user's environment, availability, and interests. Avoid common "
        "choices like gardening or cooking. For each, explain why it fits and include a local twist or activity."
        "Incorporate additional input from the user to maybe override certain preference or add new ones."
    )

async def get_user(user_id: str) -> Optional[DBUser]:
    users_col = MongoManager.get_collection("users")
    doc = await users_col.find_one({"name": user_id})
    if doc:
        doc["id"] = str(doc["_id"])
        return DBUser(**doc)
    return None

async def suggest_hobbies(data: HobbyPrompt) -> str:
    db_user = await get_user(data.user_id)
    user = safe_dbuser_to_user(db_user)
    print("Found the user details from DB for : ", user.name)
    if not user:
        raise ValueError("User not found.")

    prompt = craft_prompt(user, data.extra_prompt)
    return await generate_hobby_suggestions(prompt)
