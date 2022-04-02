from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel
from dataclasses import dataclass


class Rate(BaseModel):
    energy: float
    time: float
    transaction: float


class ChargeDetailRecord(BaseModel):
    meterStart: int
    timestampStart: datetime
    meterStop: int
    timestampStop: datetime


class CdrTransaction(BaseModel):
    cdr: ChargeDetailRecord
    rate: Rate


class Components(BaseModel):
    energy: float
    time: float
    transaction: float


class TransactionResult(BaseModel):
    overall: float
    components: Components


# ----------- improvement of service

class UpdateRate(BaseModel):
    stationId: int
    energy: float
    time: float
    transaction: float


class UpdateRateResponse(BaseModel):
    status: bool


class CrdStartTransaction(BaseModel):
    stationId: int
    meterStart: int
    timestampStart: datetime


class CrdStopTransaction(BaseModel):
    stationId: int
    chargingId: int
    meterStop: int
    timestampStop: datetime


class StartEventResponce(BaseModel):
    stationId: int
    chargingId: int
    status: bool


class StopEventResponce(BaseModel):
    stationId: int
    chargingId: int
    status: bool
    transactionResult: Optional[TransactionResult]
