from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.dual_persona import DualPersona

app = FastAPI(title="SYNAPSE AI Backend")

# CORS পারমিশন (অ্যাপের সাথে কানেকশনের জন্য)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

persona_manager = DualPersona()

# Request Models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "siam_user"

class SwitchRequest(BaseModel):
    persona: str

# 1. Health Check Endpoint
@app.get("/")
@app.get("/health")
def health_check():
    return {"status": "healthy", "current_persona": persona_manager.get_current_persona_info()}

# 2. Persona Switch Endpoint
@app.post("/switch")
def switch_persona(req: SwitchRequest):
    result = persona_manager.switch_persona(req.persona)
    return {"status": "success", "message": result, "info": persona_manager.get_current_persona_info()}

# 3. Chat Endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    current_info = persona_manager.get_current_persona_info()
    speaker_name = current_info["name"]
    
    # ব্যাকএন্ড চ্যাট রেসপন্স
    reply_text = f"[{speaker_name}]: দোস্ত, তোর কথা শুনতে পাইছি! তুই বলছিস: '{req.message}'"
    
    return {
        "reply": reply_text,
        "persona": current_info
}
