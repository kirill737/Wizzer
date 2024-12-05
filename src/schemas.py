from typing import List

from pydantic import BaseModel, Field


class DeviceRequest(BaseModel):
    user_query: str = Field(..., min_length=1)
    top_k: int = Field(50, gt=0)


class DeviceResponse(BaseModel):
    price_order: List[dict]
    rating_order: List[dict]
    statistics: dict