
from app.schemas.schemas import Rate, ChargeDetailRecord, StartEventResponce, CrdStartTransaction, CrdStopTransaction, StopEventResponce, UpdateRateResponse, UpdateRate
from logging.config import dictConfig
from app.config.log_config import log_config
import logging
from app.adapter.repositories import ChargeRepo, RateRepo
from app.Services.Calculator import CdrCalculator

dictConfig(log_config)
logger = logging.getLogger(__name__)


class ChargingService:

    @staticmethod
    def update_rate(rate: UpdateRate, db):
        res = UpdateRateResponse(status=False)
        try:
            charge_res = RateRepo.create(db, rate)
            res.status = True
        except Exception as e:
            logger.warning(f'error when try update rate of the station data={UpdateRate} error={e}')
        return res

    @staticmethod
    def start_event(cdr_transaction_start: CrdStartTransaction, db):
        res = StartEventResponce(stationId=-1, chargingId=-1, status=False)
        try:
            charge_res = ChargeRepo.create(db, cdr_transaction_start)
            res.stationId = charge_res.station_id
            res.status = True
            res.chargingId = charge_res.id
        except Exception as e:
            res.status = False
            logger.warning(f'error when try add start event of charging process data={cdr_transaction_start} error={e}')

        return res

    @staticmethod
    def stop_event(cdr_transaction_end: CrdStopTransaction, db):
        res = StopEventResponce(stationId=-1, chargingId=-1, status=False)
        try:
            charge_db = ChargeRepo.fetch_by_id(db, cdr_transaction_end.chargingId)
            charge_db.meterStop = cdr_transaction_end.meterStop
            charge_db.timestampStop = cdr_transaction_end.timestampStop

            rate_db = RateRepo.fetch_by_id(db, cdr_transaction_end.stationId)

            rate = Rate(energy=rate_db.energy, time=rate_db.time, transaction=rate_db.transaction)
            cdrDetail = ChargeDetailRecord(meterStart=charge_db.meterStart, timestampStart=charge_db.timestampStart,
                                           meterStop=charge_db.meterStop, timestampStop=charge_db.timestampStop)
            cdrCalculator = CdrCalculator(rate)
            trans_res = cdrCalculator.calculate_price(cdrDetail)

            charge_db.energy_price = trans_res.components.energy
            charge_db.time_price = trans_res.components.time
            charge_db.transaction_price = trans_res.components.transaction
            charge_db.overall = trans_res.overall
            ChargeRepo.update(db, charge_db)

            res.stationId = charge_db.station_id
            res.chargingId = charge_db.id
            res.status = True
            res.transactionResult = trans_res

        except Exception as e:
            res.status = False
            logger.warning(f'error when try add end event of charging process data={cdr_transaction_end} error={e}')

        return res