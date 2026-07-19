import os
import json
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict

# ===== আমাদের মডিউলগুলো (রেন্ডার ফিক্স সহ) =====
from src.dual_persona import DualPersona
from src.language_router import LanguageRouter

# ===== এনভায়রনমেন্ট =====
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in environment variables!")

# ===== ফাস্টএপিআই অ্যাপ =====
app = FastAPI(
    title="SYNAPSE AI API",
    version="4.0",
    description="মাল্টি-পার্সোনা ও বহুভাষিক AI অ্যাসিস্ট্যান্ট"
)

# ===== মডিউল লোড =====
persona = DualPersona()
language_router = LanguageRouter()

# ===== WebSocket ম্যানেজার =====
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
            except Exception as e:
                print(f"⚠️ Error sending message: {e}")

manager = ConnectionManager()

# ===== ১. চ্যাট এন্ডপয়েন্ট (HTTP) =====
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class ChatResponse(BaseModel):
    reply: str
    persona: str
    language: str
    language_code: str
    status: str = "success"

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        lang_info = language_router.detect_language(request.message)
        lang_code = [k for k, v in language_router.supported_languages.items() if v == lang_info][0]
        base_prompt = persona.get_system_prompt()
        final_prompt = language_router.get_language_specific_prompt(
            text=request.message,
            base_prompt=base_prompt
        )
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=final_prompt
        )
        response = model.generate_content(request.message)
        return ChatResponse(
            reply=response.text,
            persona=persona.name,
            language=lang_info["name"],
            language_code=lang_code
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

# ===== ২. চরিত্র পরিবর্তন =====
class SwitchRequest(BaseModel):
    persona: str

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

# ===== ৩. বর্তমান ক্যারেক্টারের তথ্য =====
@app.get("/persona")
async def get_persona():
    return {
        "status": "success",
        "persona": persona.get_current_persona_info()
    }

# ===== ৪. ভাষা ডিটেক্ট (ডিবাগের জন্য) =====
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

# ===== ৫. WebSocket এন্ডপয়েন্ট (রিয়েল-টাইম) =====
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    
    await manager.send_message(user_id, {
        "type": "system",
        "message": f"👋 হ্যালো {user_id}! SYNAPSE AI-তে স্বাগতম।",
        "persona": persona.name
    })

    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            
            if json_data.get("type") == "chat":
                user_message = json_data.get("message", "")
                
                lang_info = language_router.detect_language(user_message)
                lang_code = [k for k, v in language_router.supported_languages.items() if v == lang_info][0]
                
                base_prompt = persona.get_system_prompt()
                final_prompt = language_router.get_language_specific_prompt(
                    text=user_message,
                    base_prompt=base_prompt
                )
                
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=final_prompt
                )
                response = model.generate_content(user_message)
                
                await manager.send_message(user_id, {
                    "type": "reply",
                    "message": response.text,
                    "persona": persona.name,
                    "language": lang_info["name"],
                    "language_code": lang_code
                })
            
            elif json_data.get("type") == "switch":
                new_persona = json_data.get("persona", "")
                result = persona.switch_persona(new_persona)
                await manager.send_message(user_id, {
                    "type": "system",
                    "message": result,
                    "persona": persona.name
                })

    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"⚠️ WebSocket error: {e}")
        manager.disconnect(user_id)

# ===== ৬. পিং/পং (সংযোগ সচল রাখতে) =====
@app.websocket("/ws/ping")
async def ping_pong(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_text("pong")
    except WebSocketDisconnect:
        pass

# ===== ۷. রুট চেক =====
@app.get("/")
async def root():
    return {
        "message": "SYNAPSE AI API is live!",
        "version": "4.0",
        "status": "connected",
        "current_persona": persona.name,
        "docs": "/docs",
        "websocket": "ws://your-url/ws/{user_id}"
    }

# ===== ৮. হেলথ চেক =====
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "python": os.sys.version,
        "persona": persona.name
    }
