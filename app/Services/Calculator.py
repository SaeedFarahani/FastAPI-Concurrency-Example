
from app.schemas.schemas import TransactionResult, Rate, ChargeDetailRecord,Components


class CdrCalculator:
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
        hours = duration_in_s / 3600
        energy = (cdr.meterStop - cdr.meterStart) / 1000

        time_price = round(hours * self.time_rate, 3)
        energy_price = round(energy * self.energy_rate, 3)
        transaction_price = round(self.transaction_rate, 3)
        overall_pirce = round(time_price + energy_price + transaction_price, 2)
        components = Components(energy=energy_price, time=time_price, transaction=transaction_price)
        return TransactionResult(components=components, overall=overall_pirce)




