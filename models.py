# SOURCE https://analyzingalpha.com/create-an-equities-database#undefined
# FILENAME models.py

from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, BigInteger, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, UniqueConstraint
import enum


Base = declarative_base()

class PriceFrequency(enum.Enum):
	daily = 'daily'
	weekly = 'weekly'
	monthly = 'monthly'
	quarterly = 'quarterly'
	yearly = 'yearly'

class Security(Base):
	__tablename__ = 'security'
	id = Column(Integer, primary_key=True, autoincrement=True)
	id_intrinio = Column('id_intrinio', String(10), unique=True, nullable=False)
	code = Column('code', String(3), nullable=False)
	currency = Column('currency', String(3), nullable=False)
	ticker = Column('ticker', String(12), nullable=False)
	name = Column('name', String(200), nullable=False)
	figi = Column('figi', String(12))
	composite_figi = Column('composite_figi', String(12))
	share_class_figi = Column(Integer, ForeignKey('exchange.id',
	                                    onupdate="CASCADE",
	                                    ondelete="SET NULL"))
	has_invalid_data = Column('has_invalid_data', Boolean)
	has_missing_company = Column('has_missing_company', Boolean)
	exchange = relationship('Exchange')
	company = relationship('Company')

class Exchange(Base):
	__tablename__ = 'exchange'
	id = Column(Integer, primary_key=True, autoincrement=True)
	mic = Column('mic', String(10), unique=True, nullable=False)
	acronym = Column('acronym', String(20), nullable=False)
	name = Column('name', String(200), nullable=False)
	security = relationship('Security')

class SecurityPrice(Base):
	__tablename__ = 'security_price'
	id = Column(Integer, primary_key=True)
	date = Column('date', Date, nullable=False)
	open = Column('open', Float)
	high = Column('high', Float)
	low = Column('low', Float)
	close = Column('close', Float)
	volume = Column('volume', BigInteger)
	adj_open = Column('adj_open', Float)
	adj_high = Column('adj_high', Float)
	adj_low = Column('adj_low', Float)
	adj_close = Column('adj_close', Float)
	adj_volume = Column('adj_volume', BigInteger)
	intraperiod = Column('intraperiod', Boolean, nullable=False)
	frequency = Column('frequency', Enum(PriceFrequency), nullable=False)
	security_id = Column(Integer, ForeignKey('security.id',
	                                         onupdate="CASCADE",
	                                         ondelete="CASCADE"),
	                                         nullable=False)
	UniqueConstraint('date', 'security_id')
	security_id = relationship('Security')

class StockAdjustment(Base):
	__tablename__ = 'stock_adjustment'
	id = Column(Integer, primary_key=True)
	date = Column('date', Date, nullable=False)
	factor = Column('factor', Float, nullable=False)
	dividend = Column('divident', float)
	split_ratio = Column('split_ratio', Float)
	security_id = Column(Integer, ForeignKey('security.id',
	                                         onupdate="CASCADE",
	                                         ondelete="CASCADE"),
	                                         nullable=False)
	security_id = relationship('Security')
	
class Company(Base):
	__tablename__ = 'company'
	id = Column(Integer, primary_key=True)
	name = Column('name', String(100), nullable=False)
	cik = Column('cik', String(10))
	description = Column('description', String(2000))
	company_url = Column('company_url', String(100))
	sic = Column('sic', String(200))
	industry_category = Column('industry_category', String(200))
	industry_group = Column('industry_group', String(200))
	security_id = Column(Integer, ForeignKey('security.id',
	                                         onupdate="CASCADE",
	                                         ondelete="CASCADE"),
	                                         nullable=False)
	security_id = relationship('Security')
	
	