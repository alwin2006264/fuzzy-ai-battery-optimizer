from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from ai_parser import parse_battery_text
from fuzzy_system import FuzzyBatteryOptimizer


# ---------------------------------------------------------
# Create FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Fuzzy AI Smartphone Battery Optimizer",
    description="AI + Fuzzy Logic battery optimization API",
    version="1.0.0",
)


# ---------------------------------------------------------
# Enable CORS
# This allows the React frontend to communicate with
# the Python backend.
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request model
# ---------------------------------------------------------

class BatteryRequest(BaseModel):
    text: str = Field(
        min_length=1,
        description="Natural-language description of smartphone usage"
    )


# ---------------------------------------------------------
# Create fuzzy optimizer
# ---------------------------------------------------------

optimizer = FuzzyBatteryOptimizer()


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Fuzzy AI Battery Optimizer API is running"
    }


# ---------------------------------------------------------
# Main battery analysis endpoint
# ---------------------------------------------------------

@app.post("/analyze")
def analyze_battery(request: BatteryRequest):

    try:

        # ---------------------------------------------
        # Step 1: Gemini + LangChain
        # ---------------------------------------------

        ai_inputs = parse_battery_text(request.text)


        # ---------------------------------------------
        # Step 2: Fuzzy Logic
        # ---------------------------------------------

        fuzzy_result = optimizer.calculate_power_saving(
            battery=ai_inputs.battery_level,
            app_usage=ai_inputs.app_usage,
            screen_usage=ai_inputs.screen_usage,
            network_usage=ai_inputs.network_usage,
            temperature=ai_inputs.temperature,
        )


        # ---------------------------------------------
        # Step 3: Return combined result
        # ---------------------------------------------

        return {
            "success": True,

            "ai_inputs": ai_inputs.model_dump(),

            "fuzzy_result": fuzzy_result,
        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )