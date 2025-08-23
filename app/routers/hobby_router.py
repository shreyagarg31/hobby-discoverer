from fastapi import APIRouter, Depends, HTTPException
from app.models.hobby import HobbyPrompt, HobbySuggestion
from app.services.hobby_service import suggest_hobbies

router = APIRouter()

@router.post("/hobby/suggest", response_model=HobbySuggestion)
async def hobby_suggest_endpoint(data: HobbyPrompt):
    print("Received the request for hobby suggestions.")
    try:
        text = await suggest_hobbies(data)
        return HobbySuggestion(suggestions=text)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get hobby suggestions.")
