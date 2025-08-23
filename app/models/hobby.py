from pydantic import BaseModel


class HobbyPrompt(BaseModel):
    user_id: str
    extra_prompt: str

class HobbySuggestion(BaseModel):
    suggestions: str