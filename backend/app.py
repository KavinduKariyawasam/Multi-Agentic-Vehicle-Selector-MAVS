# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from starlette.concurrency import run_in_threadpool
from dotenv import load_dotenv

from crew import VehicleRecommenderCrew, ValidationError, VehicleRecommenderError
from logger.logger import logger

import os
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

load_dotenv()

app = FastAPI(title="Vehicle Recommender API", version="1.0.0")

# CORS (tune for your frontend origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL(s) in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    location: str = Field(..., examples=["USA"])
    budget: str | int | float = Field(..., examples=["40000"])
    allowed_sites: Optional[List[str]] = Field(
        default=None,
        description="Optional list of manufacturer domains to restrict scraping."
    )

class RecommendResponse(BaseModel):
    ok: bool
    result: Any
    meta: Dict[str, Any]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/recommend", response_model=RecommendResponse)
async def recommend(payload: RecommendRequest):
    try:
        # If you want to pass allowed_sites into data_agent later, add plumbing in crew/tasks.
        crew = VehicleRecommenderCrew(payload.location, payload.budget)

        # crew.run() is synchronous and potentially heavy; run it in a thread
        result = await run_in_threadpool(crew.run)

        return RecommendResponse(
            ok=True,
            result=result,
            meta={
                "location": payload.location,
                "budget": str(payload.budget),
            },
        )

    except ValidationError as ve:
        logger.warning("Validation failed: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve)) from ve

    except VehicleRecommenderError as vre:
        logger.error("Crew error: %s", vre)
        raise HTTPException(status_code=500, detail=str(vre)) from vre

    except Exception as e:
        logger.exception("Unhandled error during /api/recommend")
        raise HTTPException(status_code=500, detail="Internal server error") from e
