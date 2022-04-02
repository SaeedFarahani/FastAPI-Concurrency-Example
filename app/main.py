import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from logging.config import dictConfig
from app.config.log_config import log_config
import logging

from sqlalchemy.orm import Session
# from test import test_api
import time
from app.Services.Calculator import CdrCalculator
from app.Services.ChargingService import ChargingService
from app.adapter.db import get_db, engine
from app.domain import models

from schemas import schemas

dictConfig(log_config)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0", )

models.Base.metadata.create_all(bind=engine)


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


@app.post('/calculate-price', tags=["CRD"], response_model=schemas.TransactionResult, status_code=200)
async def calculate_price(cdr_transaction_input: schemas.CdrTransaction):
    """
        calculate price by charge detail record and rates as inputs
    """
    calculator = CdrCalculator(cdr_transaction_input.rate)
    return calculator.calculate_price(cdr_transaction_input.cdr)


#  -------  improvement

@app.post('/update_rates', tags=["CRD"], status_code=200)
async def update_rates(rate: schemas.UpdateRate, db: Session = Depends(get_db)):
    """
        set rates with independent servie
    """

    return ChargingService.update_rate(rate, db)


@app.post('/start-event', tags=["CRD"], response_model=schemas.StartEventResponce, status_code=200)
async def start_event(cdr_transaction_start: schemas.CrdStartTransaction, db: Session = Depends(get_db)):
    """
        charging station send start event
    """
    return ChargingService.start_event(cdr_transaction_start, db)


@app.post('/end-event', tags=["CRD"], response_model=schemas.StopEventResponce, status_code=200)
async def end_event(cdr_transaction_end: schemas.CrdStopTransaction, db: Session = Depends(get_db)):
    """
        charging station send stop event
    """
    return ChargingService.stop_event(cdr_transaction_end, db)


@app.post('/price-at-moment', tags=["CRD"], response_model=schemas.StopEventResponce, status_code=200)
async def price_at_moment(cdr_transaction_end: schemas.CrdStopTransaction):
    """
        charging station calculate price at moment
    """
    return schemas.StopEventResponce()


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
