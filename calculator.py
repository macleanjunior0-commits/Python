import math
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Calculator API")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class CalculationRequest(BaseModel):
    a: float = Field(allow_inf_nan=False)
    b: float = Field(allow_inf_nan=False)
    operation: Literal["add", "subtract", "multiply", "divide"]


@app.get("/", include_in_schema=False)
def calculator_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/calc")
def calculate(request: CalculationRequest) -> dict[str, float]:
    if request.operation == "add":
        result = request.a + request.b
    elif request.operation == "subtract":
        result = request.a - request.b
    elif request.operation == "multiply":
        result = request.a * request.b
    else:
        if request.b == 0:
            raise HTTPException(status_code=422, detail="Cannot divide by zero.")
        result = request.a / request.b

    if not math.isfinite(result):
        raise HTTPException(status_code=422, detail="The result is outside the supported numeric range.")

    return {"result": result}
