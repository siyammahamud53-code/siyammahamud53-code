import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# ===== আমাদের মডিউলগুলো ইম্পোর্ট (রেন্ডার ফিক্স সহ) =====
from src.dual_persona import DualPersona
from src.language_router import LanguageRouter

# ===== ১. এনভায়রনমেন্ট লোড ও জেমিনি কনফিগ =====
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in environment variables!")

# ===== ২. ফাস্টএপিআই অ্যাপ =====
app = FastAPI(
    title="SYNAPSE AI API",
    version="4.0",
    description="মাল্টি-পার্সোনা ও বহুভাষিক AI অ্যাসিস্ট্যান্ট"
)

# ===== ৩. ক্যারেক্টার ও ভাষা ইঞ্জিন লোড =====
persona = DualPersona()
language_router = LanguageRouter()

# ===== ৪. রিকোয়েস্ট ও রেসপন্স মডেল =====
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"  # ভবিষ্যতে মাল্টি-ইউজারের জন্য

class ChatResponse(BaseModel):
    reply: str
    persona: str           # বর্তমান ক্যারেক্টারের নাম
    language: str          # ডিটেক্ট করা ভাষা
    language_code: str     # ভাষার কোড (bn, en, hi ইত্যাদি)
    status: str = "success"

# ===== ৫. চ্যাট এন্ডপয়েন্ট =====
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # ১. ভাষা ডিটেক্ট করা
        lang_info = language_router.detect_language(request.message)
        lang_code = [k for k, v in language_router.supported_languages.items() if v == lang_info][0]
        
        # ২. সিস্টেম প্রম্পট তৈরি (পার্সোনা + ভাষা)
        base_prompt = persona.get_system_prompt()
        final_prompt = language_router.get_language_specific_prompt(
            text=request.message,
            base_prompt=base_prompt
        )
        
        # ৩. জেমিনি মডেল ইনিশিয়ালাইজ
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=final_prompt
        )
        
        # ৪. রেসপন্স জেনারেট
        response = model.generate_content(request.message)
        
        # ৫. রেসপন্স রিটার্ন (ব্যক্তিত্ব ও ভাষার তথ্য সহ)
        return ChatResponse(
            reply=response.text,
            persona=persona.name,
            language=lang_info["name"],
            language_code=lang_code
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

# ===== ৬. চরিত্র পরিবর্তনের এন্ডপয়েন্ট =====
class SwitchRequest(BaseModel):
    persona: str  # 'ragna' অথবা 'maya'

@app.post("/switch")
async def switch_persona(request: SwitchRequest):
    result = persona.switch_persona(request.persona)
    if "✅" in result:
        return {
            "status": "success",
            "message": result,
            "current_persona": persona.get_current_persona_info()
        }
    else:
        raise HTTPException(status_code=400, detail=result)

# ===== ৭. বর্তমান ক্যারেক্টারের তথ্য =====
@app.get("/persona")
async def get_persona():
    return {
        "status": "success",
        "persona": persona.get_current_persona_info()
    }

# ===== ৮. ভাষা ডিটেক্ট টেস্ট (ডিবাগের জন্য) =====
class DetectRequest(BaseModel):
    text: str

@app.post("/detect-language")
async def detect_language(request: DetectRequest):
    lang_info = language_router.detect_language(request.text)
    lang_code = [k for k, v in language_router.supported_languages.items() if v == lang_info][0]
    return {
        "status": "success",
        "text": request.text[:100],
        "language": lang_info["name"],
        "language_code": lang_code,
        "flag": lang_info["flag"]
    }

# ===== ৯. রুট চেক =====
@app.get("/")
async def root():
    return {
        "message": "SYNAPSE AI API is live!",
        "version": "4.0",
        "status": "connected",
        "current_persona": persona.name,
        "docs": "/docs"
    }

# ===== ১০. হেলথ চেক =====
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "python": os.sys.version,
        "persona": persona.name
    }
