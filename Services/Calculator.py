
from entrypoints.schemas import CdrTransaction, TransactionResult, Rate, ChargeDetailRecord,Components


class Calculator:
    energy_rate: float
    time_rate: float
    transaction_rate: float

    def __init__(self, rate: Rate):
        self.energy_rate = rate.energy
        self.time_rate = rate.time
        self.transaction_rate = rate.transaction

    def calculate_price(self, cdr: ChargeDetailRecord):
        total_time = cdr.timestampStop - cdr.timestampStart
        duration_in_s = total_time.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]
        energy = cdr.meterStop - cdr.meterStart
        component = Components()
        component.time = round(hours * self.time_rate, 3)
        component.energy = round(energy * self.energy_rate, 3)
        component.transaction = round(self.transaction_rate, 3)
        return TransactionResult(component)