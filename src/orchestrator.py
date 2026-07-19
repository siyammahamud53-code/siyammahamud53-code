import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_file

# এনভায়রনমেন্ট ভ্যারিয়েবল লোড করা
load_file()

app = FastAPI(
    title="Siam AI Universal Assistant Backend",
    description="FastAPI backend for controlling mobile automation, game settings, and voice control via Gemini API.",
    version="1.0.0"
)

# CORS সেটিংস (যাতে যেকোনো ডিভাইস বা ফ্রন্টএন্ড থেকে কানেক্ট করা যায়)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# জেমিনি এআই কনফিগারেশন
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

class UserMessage(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Siam's Universal AI Server is running flawlessly!",
        "gemini_connected": model is not None
    }

@app.post("/api/chat")
async def chat_with_ai(data: UserMessage):
    if not model:
        return {"error": "Gemini API key is missing or not configured in Render!"}
    
    try:
        # ৪০টি ইউনিভার্সাল মোড ও ধাপের প্রম্পট লজিক এখানে যুক্ত হবে
        response = model.generate_content(data.message)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
