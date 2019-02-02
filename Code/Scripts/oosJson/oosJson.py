import argparse
parser = argparse.ArgumentParser()
parser.add_argument("paramNames", help="names and order of parameters")
parser.add_argument("oosString", help="convert TradeStation OOS date to json")
#parser.add_argument("oosString", help="convert TradeStation OOS date to json", nargs=argparse.REMAINDER)
args = parser.parse_args()
#print(args.oosString)

print(f'paramNames: {args.paramNames}')
pd = 0
for line in args.oosString.splitlines():
  pd += 1
  print(f'line {pd}: {line}')
  fields = line.split()
  print(f'fields: {fields}')
  params = fields[0]
  print(f'params: {params}')
  #start_dt,tmp,end_dt = params[1].split("\s")
  #d[pd] = { 'start_dt': f'{start_dt}',
  #          'end_dt' : f'{end_dt}'
  #        }
            

'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
import sys
sys.path.append("..")
from model.base import Base
from model.session import Session
from model.prototype import Prototype
 
DATABASE_URL="postgres://hiikokjjrwmqpg:ff6d83e0795990ffb048d526caf295eaad7a45476691991f989be513d4e3a6bb@ec2-54-83-60-13.compute-1.amazonaws.com:5432/d617hc9tos6o76"

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
query = session.query(Prototype).filter(Prototype.id == 4)
print(query.first().in_sample_file)
''' 
