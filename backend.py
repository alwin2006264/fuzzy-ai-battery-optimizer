from fastapi import FastAPI
from pydantic import BaseModel
from main import analyze_battery


app = FastAPI(
    title="Fuzzy AI Battery Optimizer API"
)


class BatteryRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Fuzzy AI Battery Optimizer API is running"
    }


@app.post("/analyze")
def analyze(request: BatteryRequest):

    result = analyze_battery(request.text)

    return {
        "status": "success",
        "ai_inputs": result["ai_inputs"],
        "fuzzy_result": result["fuzzy_result"]
    }