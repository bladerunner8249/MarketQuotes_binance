# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 15:25:15 2017

@author: Administrator
"""
import pymongo
import time
import traceback
from pymongo.helpers import DuplicateKeyError
from MarketQuotes import MarketQuotes
from datetime import datetime

CONNECTOIN = pymongo.MongoClient('192.168.0.22',27017)

def comb(ts,data):
    head = ts/1000
    #tail = ts%1000
    normal_time = datetime.fromtimestamp(head).strftime('%Y-%m-%d %H:%M:%S')
    #normal_time  = normal_time+'.'+str(tail)
    kline = {'_id':normal_time,
             'Open':data[0],
             'High':data[1],
             'Low':data[2],
             'Close': data[3],
             'Volume':data[4],
             'Number_of_trades':data[6],
             'Taker_buy_base_asset_volume':data[7],
             'Taker_buy_quote_asset_volume':data[8]
             }
    return kline

def writeMongo(instance,dbName,former):
    candle = instance.kline('1m')[0]
    if len(candle)==12:        
        ts = candle[0]; data = candle[1:]
        if data != former:
            former = data
            conn = CONNECTOIN[dbName]
            table = conn[instance.get_attribute()]
            x = data#.copy()
            #print x
            table.insert_one(comb(ts,x))
    else:pass
    return former 
    
if __name__ == "__main__":
    BTC = MarketQuotes('BTCUSDT')   
    dbName = 'binance'
   
    former1 = []
    delaysec=30
    
    while True:
    #for i in range(10):
        try:
            former1 = writeMongo(BTC,dbName,former1)
            time.sleep(delaysec)
        except DuplicateKeyError:
            time.sleep(delaysec)
        except:
            errorFile = open('binance_error.txt','a')
            errorFile.write(traceback.format_exc())
            errorFile.write("\n")
            errorFile.close()

            