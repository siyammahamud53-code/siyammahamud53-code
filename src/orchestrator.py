import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# ===== ১. এনভায়রনমেন্ট লোড ও জেমিনি কনফিগার =====
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in environment variables!")

# ===== ২. ফাস্টএপিআই অ্যাপ =====
app = FastAPI(
    title="SYNAPSE AI API",
    version="4.0",
    description="মাল্টি-পার্সোনা AI অ্যাসিস্ট্যান্ট"
)

# ===== ৩. রিকোয়েস্ট ও রেসপন্স মডেল =====
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"  # ভবিষ্যতে মাল্টি-ইউজারের জন্য

class ChatResponse(BaseModel):
    reply: str
    status: str = "success"

# ===== ৪. চ্যাট এন্ডপয়েন্ট =====
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # জেমিনি মডেল ইনিশিয়ালাইজ
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="আপনি SYNAPSE AI, একজন বুদ্ধিমান ও বন্ধুসুলভ সহকারী। আপনি বাংলা ও ইংরেজি উভয় ভাষায় উত্তর দিতে পারেন।"
        )
        # রেসপন্স জেনারেট
        response = model.generate_content(request.message)
        return ChatResponse(reply=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

# ===== ৫. রুট চেক =====
@app.get("/")
async def root():
    return {
        "message": "SYNAPSE AI API is live!",
        "version": "4.0",
        "status": "connected",
        "docs": "/docs"
    }

# ===== ৬. হেলথ চেক (আপনার UptimeRobot-এর জন্য) =====
@app.get("/health")
async def health_check():
    return {"status": "healthy", "python": os.sys.version}
