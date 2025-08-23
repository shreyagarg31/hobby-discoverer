import os
import httpx

# Initialize the GenAI client using your Gemini API key
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
api_key=os.getenv("GEMINI_API_KEY")
URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

import traceback

async def generate_hobby_suggestions(prompt: str) -> str:
     payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
     headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": os.getenv("GEMINI_API_KEY"),
    }
     async with httpx.AsyncClient(timeout=60.0) as client:
        print("Calling AI API for hobby generation")
        try:
            model = "gemini-1.5-flash"
            full_url = URL.format(model=model)
            print("URL:", full_url)
            response = await client.post(full_url, json=payload, headers=headers)
            print("Status:", response.status_code)
            response.raise_for_status()
            data = response.json()
            if 'candidates' in data and data['candidates']:
                parts = data['candidates'][0].get('content', {}).get('parts', [])
                if parts:
                    return parts[0].get('text', "")
            return ""
        except Exception as e:
            print("HTTP Status Error:", str(e))
            print(traceback.format_exc())
            return None

