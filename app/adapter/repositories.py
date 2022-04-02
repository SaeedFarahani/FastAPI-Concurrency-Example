from sqlalchemy.orm import Session
from app.schemas import schemas
from app.domain import models


class ChargeRepo:
    async def create(db: Session, item: schemas.CrdStartTransaction):
        db_item = models.Charge(station_id=item.stationId, meterStart=item.meterStart,
                                timestampStart=item.timestampStart)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def fetch_by_id(db: Session, charge_id):
        return db.query(models.Charge).filter(models.Charge.id == charge_id).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Charge).offset(skip).limit(limit).all()

    async def delete(db: Session, charge_id):
        db_item = db.query(models.Charge).filter_by(id=charge_id).first()
        db.delete(db_item)
        db.commit()

    async def update(db: Session, item_data):
        updated_item = db.merge(item_data)
        db.commit()
        return updated_item


class RateRepo:
    async def create(db: Session, item: schemas.UpdateRate):
        db_item = models.Rate(station_id=item.stationId, energy_price=item.energy, time_price=item.time,
                              transaction_price=item.transaction)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def fetch_by_stationId(db: Session, station_id):
        return db.query(models.Rate).filter(models.Rate.station_id == station_id).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Rate).offset(skip).limit(limit).all()

    async def delete(db: Session, _id):
        db_item = db.query(models.Rate).filter_by(id=_id).first()
        db.delete(db_item)
        db.commit()

    async def update(db: Session, item_data):
        updated_item = db.merge(item_data)
        db.commit()
        return updated_item
