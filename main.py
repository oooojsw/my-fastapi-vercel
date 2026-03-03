from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI()


class ChatRequest(BaseModel):
    name: str
    question: str
    max_length: int = 100


class CreateAgentRequest(BaseModel):
    agent_name: str
    personality: str
    power: int


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
