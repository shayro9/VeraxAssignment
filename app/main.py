from fastapi import FastAPI
from app.engine import MitigationEngine
from pydantic import BaseModel


class MitigateRequest(BaseModel):
    prompt: str
    user_id: str


app = FastAPI(title="VeraxHomeAssignment")

engine = MitigationEngine()


@app.get("/")
def read_root():
    return {"message": "Hello world"}


@app.post("/mitigate")
async def mitigate_prompt(request: MitigateRequest):
    result = engine.mitigate(request.user_id, request.prompt)
    return result


@app.get("/history")
async def get_history(n: int = 20):
    return engine.get_history(n)


@app.post("/reload")
async def reload_config():
    engine.load_policy()
    return {"status": "Policy reloaded successfully"}
