from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
# from test import test_api
import time
import asyncio

import schemas

app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0", )



@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print('inside middleware!')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


@app.post('/calculate-price', tags=["Item"], response_model=schemas.TransactionResult, status_code=201)
async def calculate_price(item_request: schemas.CdrTransaction):
    """
   calculate price by charge detail record and rates as inputs
    """
    return schemas.Results()


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
