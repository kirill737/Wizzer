from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.processing import get_device_info
from src.schemas import (
    DeviceRequest,
    DeviceResponse,
)


origins = ["http://localhost"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ready")
async def ready() -> str:
    return "ok"


@app.get("/live")
async def live() -> str:
    return "ok"


@app.post("/device")
async def device_endpoint(body: DeviceRequest) -> DeviceResponse:
    try:
        device_info = await get_device_info(body)
        return DeviceResponse(**device_info)
    except ValueError as e:
        message = str(e)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=message)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Что-то пошло не так")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
