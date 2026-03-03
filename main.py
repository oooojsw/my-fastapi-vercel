from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import os
import time

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists(os.path.join(BASE_DIR, "static")):
    app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"[日志] {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response


class ChatRequest(BaseModel):
    name: str
    question: str
    max_length: int = 100


class CreateAgentRequest(BaseModel):
    agent_name: str
    personality: str
    power: int


@app.get("/")
async def root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.post("/chat")
def start_chat(request: ChatRequest):
    user_msg = request.question
    user_name = request.name
    
    ai_reply = f"你好 {user_name}！关于你问的'{user_msg}'，我的回答是：这太简单了！"
    
    return {"reply": ai_reply, "status": "success"}


@app.post("/create_agent")
def create_agent(request: CreateAgentRequest):
    return {
        "message": f"Agent {request.personality}的{request.agent_name} 创建成功，战斗力为 {request.power}！"
    }


@app.post("/ask_ai")
async def ask_ai(question: str):
    await asyncio.sleep(3)
    
    return {"answer": f"你问了：{question}。AI 思考 3 秒后觉得你很帅！"}


@app.post("/ask_ai_batch")
async def ask_ai_batch(questions: list[str]):
    async def single_ask(q: str):
        await asyncio.sleep(3)
        return f"你问了：{q}。AI 回答你！"
    
    results = await asyncio.gather(*[single_ask(q) for q in questions])
    
    return {"answers": results}
