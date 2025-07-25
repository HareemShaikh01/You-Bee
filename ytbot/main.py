from fastapi import FastAPI
from pydantic import BaseModel
from rag_bot import get_bot_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (React, etc.) to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request schema
class QuestionRequest(BaseModel):
    video_id: str
    question: str

# POST endpoint
@app.post("/ask/")
async def ask_question(req: QuestionRequest):
    answer = get_bot_response(req.video_id, req.question)
    return {"answer": answer}

# Root health check
@app.get("/")
async def root():
    return {"message": "FastAPI RAG Bot is running!"}

# Local dev run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
