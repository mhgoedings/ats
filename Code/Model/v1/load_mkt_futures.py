from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from session import Session
from mkt_future import MktFuture
from prototype import Prototype
from candidate import Candidate
from strategy import Strategy
from base import Base
 
DATABASE_URL="postgres://hiikokjjrwmqpg:ff6d83e0795990ffb048d526caf295eaad7a45476691991f989be513d4e3a6bb@ec2-54-83-60-13.compute-1.amazonaws.com:5432/d617hc9tos6o76"

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
objects = [
    MktFuture(id=1,symbol='@ES',ts_symbol='@ES.D',group_1='Indices',
           name='Emini S&P 500',margin_day=500,
           value_1_tick=12.50,ticks_per_point=4),
    MktFuture(id=2,symbol='@YM',ts_symbol='@YM.D',group_1='Indices',
           name='Emini Dow 30',margin_day=500,
           value_1_tick=5.00,ticks_per_point=1),
    MktFuture(id=3,symbol='@NQ',ts_symbol='@NQ.D',group_1='Indices',
           name='Emini NASDAQ',margin_day=500,
           value_1_tick=5.00,ticks_per_point=4),
    MktFuture(id=4,symbol='@RTY',ts_symbol='@RTY.D',group_1='Indices',
           name='Emini Russell',margin_day=500,
           value_1_tick=0.10,ticks_per_point=10),
    MktFuture(id=5,symbol='@EMD',ts_symbol='@EMD.D',group_1='Indices',
           name='Emini MidCap 400',margin_day=3350,
           value_1_tick=10.00,ticks_per_point=10),
    MktFuture(id=6,symbol='@CL',ts_symbol='@CL',group_1='Energies',
           name='Crude Oil',margin_day=1012,
           value_1_tick=10.00,ticks_per_point=100),
    MktFuture(id=7,symbol='@NG',ts_symbol='@NG',group_1='Energies',
           name='Natural Gas',margin_day=1238,
           value_1_tick=10.00,ticks_per_point=10),
    MktFuture(id=8,symbol='@RB',ts_symbol='@RB',group_1='Energies',
           name='RBOB Gasoline',margin_day=2805,
           value_1_tick=4.20,ticks_per_point=100),
    MktFuture(id=9,symbol='@HO',ts_symbol='@HO',group_1='Energies',
           name='Heating Oil',margin_day=2970,
           value_1_tick=4.20,ticks_per_point=100),
    MktFuture(id=10,symbol='@GC',ts_symbol='@GC',group_1='Metals',
           name='Gold',margin_day=825,
           value_1_tick=10.00,ticks_per_point=10),
    MktFuture(id=11,symbol='@SI',ts_symbol='@SI',group_1='Metals',
           name='Silver',margin_day=6600,
           value_1_tick=25.00,ticks_per_point=200),
    MktFuture(id=12,symbol='@HG',ts_symbol='@HG',group_1='Metals',
           name='Copper',margin_day=1705,
           value_1_tick=12.50,ticks_per_point=20),

    MktFuture(id=13,symbol='@ZC',ts_symbol='@ZC',group_1='Agricultures',
           name='Corn',margin_day=1182,
           value_1_tick=12.50,ticks_per_point=4),
    MktFuture(id=14,symbol='@S',ts_symbol='@S',group_1='Agricultures',
           name='Soybeans',margin_day=1958,
           value_1_tick=12.50,ticks_per_point=4),
    MktFuture(id=15,symbol='@ZW',ts_symbol='@ZW',group_1='Agricultures',
           name='Wheat',margin_day=945,
           value_1_tick=12.50,ticks_per_point=4),
    MktFuture(id=16,symbol='@LC',ts_symbol='@LC',group_1='Agricultures',
           name='Live Cattle',margin_day=506,
           value_1_tick=10.00,ticks_per_point=40),
    MktFuture(id=17,symbol='@HE',ts_symbol='@HE',group_1='Agricultures',
           name='Live Hogs',margin_day=675,
           value_1_tick=10.00,ticks_per_point=40),
    MktFuture(id=18,symbol='@ZM',ts_symbol='@ZM',group_1='Agricultures',
           name='Soybean Meal',margin_day=1519,
           value_1_tick=10.00,ticks_per_point=10),
    MktFuture(id=19,symbol='@ZL',ts_symbol='@ZL',group_1='Agricultures',
           name='Soybean Oil',margin_day=1013,
           value_1_tick=6.00,ticks_per_point=100),
    MktFuture(id=20,symbol='@CC-M',ts_symbol='@CC-M',group_1='Agricultures',
           name='Cocoa',margin_day=550,
           value_1_tick=10.00,ticks_per_point=1),
    MktFuture(id=21,symbol='@KC-M',ts_symbol='@KC-M',group_1='Agricultures',
           name='Coffee',margin_day=1183,
           value_1_tick=18.75,ticks_per_point=20),
    MktFuture(id=22,symbol='@SB-M',ts_symbol='@SB-M',group_1='Agricultures',
           name='Sugar',margin_day=275,
           value_1_tick=11.20,ticks_per_point=100),
    MktFuture(id=23,symbol='@CT-M',ts_symbol='@CT-M',group_1='Agricultures',
           name='Cotton',margin_day=825,
           value_1_tick=5.00,ticks_per_point=100),


    MktFuture(id=24,symbol='@GE',ts_symbol='@GE',group_1='Interest Rates',
           name='Eurodollars',margin_day=358,
           value_1_tick=12.50,ticks_per_point=200),
    MktFuture(id=25,symbol='@ZB',ts_symbol='@ZB',group_1='Interest Rates',
           name='30 Year Bonds',margin_day=1980,
           value_1_tick=31.25,ticks_per_point=32),
    MktFuture(id=26,symbol='@ZN',ts_symbol='@ZN',group_1='Interest Rates',
           name='10 Year Bonds',margin_day=743,
           value_1_tick=15.625,ticks_per_point=64),
    MktFuture(id=27,symbol='@ZF',ts_symbol='@ZF',group_1='Interest Rates',
           name='5 Year Notes',margin_day=495,
           value_1_tick=15.625,ticks_per_point=64),
    MktFuture(id=28,symbol='@ZT',ts_symbol='@ZT',group_1='Interest Rates',
           name='2 Year Notes',margin_day=358,
           value_1_tick=15.625,ticks_per_point=128),
    MktFuture(id=29,symbol='@ZQ',ts_symbol='@ZQ',group_1='Interest Rates',
           name='Fed Funds',margin_day=368,
           value_1_tick=10.4175,ticks_per_point=400),
]
session.bulk_save_objects(objects)
session.commit()

