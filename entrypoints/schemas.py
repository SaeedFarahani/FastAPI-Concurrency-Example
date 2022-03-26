from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


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
    overall: int
    components: Components

    def __init__(self, components: Components):
        overall = components.time + components.transaction + components.energy
        self.overall = round(overall, 2)




