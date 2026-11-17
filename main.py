from contextlib import asynccontextmanager
import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import init_db, log_request
from llm import generate_response

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    start_time = time.perf_counter()
    
    try:
        response_text = await generate_response(req.prompt)
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        await log_request(req.prompt, response_text, latency_ms, "success")
        return {"response": response_text, "latency_ms": latency_ms}

    except Exception as exc:
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        await log_request(req.prompt, str(exc), latency_ms, "error")
        raise HTTPException(status_code=502, detail=str(exc))