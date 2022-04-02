from sqlalchemy import Column, Integer, Float, DateTime

from app.adapter.db import Base


class Rate(Base):

    __tablename__ = "Rate"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, nullable=False)
    energy_price = Column(Float)
    time_price = Column(Float)
    transaction_price = Column(Float)

    def __repr__(self):
        return f'Rate(station_id={self.station_id}) -- energy_price={self.energy_price} , ' \
               f'time_price={self.time_price}, transaction_price={self.transaction_price}'


class Charge(Base):

    __tablename__ = "Charge"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, nullable=False)
    meterStart = Column(Integer)
    timestampStart = Column(DateTime(timezone=True))
    meterStop = Column(Integer)
    timestampStop = Column(DateTime(timezone=True))
    energy_price = Column(Float)
    time_price = Column(Float)
    transaction_price = Column(Float)
    overall = Column(Float)

    def __repr__(self):
        return f'Charge(station_id={self.station_id}) --  meterStart={self.meterStart} , ' \
               f'meterStop={self.meterStop} , overall={self.overall}'
