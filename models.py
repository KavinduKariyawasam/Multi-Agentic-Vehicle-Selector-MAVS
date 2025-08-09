from pydantic import BaseModel, Field
from typing import List


class VehicleSpec(BaseModel):
    """Structured representation of a single vehicle and its specifications."""

    year: int = Field(..., description="Model year")
    model_name: str = Field(..., description="Name of the vehicle model")
    trim: str = Field(..., description="Trim designation")
    price: float = Field(..., description="Manufacturer's suggested retail price (USD)")
    engine_type: str = Field(..., description="Engine configuration")
    transmission_type: str = Field(..., description="Transmission type")
    fuel_efficiency: str = Field(..., description="Fuel economy (e.g., MPG or MPGe)")
    safety_features: List[str] = Field(
        ..., description="List of key safety features"
    )


class TopPick(BaseModel):
    """Representation of a ranked recommendation."""

    rank: int = Field(..., ge=1, le=3)
    model_name: str
    trim: str
    price: float
    key_reason: str


class Recommendation(BaseModel):
    """The final recommendation payload containing top picks and analysis."""

    top_picks: List[TopPick]
    analysis: str