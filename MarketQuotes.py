# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 13:53:51 2017
symbols: 'BTCUSDT', 'ETHUSD',
@author:  bladerunner8249
"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from binance_exceptions import BinanceAPIException, BinanceRequestException
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

class MarketQuotes:
    HOST = "https://www.binance.com"
    
    def __init__(self,symbol):
        self.symbol = symbol
    
    def _get(self,url,params):
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
        session = requests.Session()
        #session.keep_alive = False
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        try:
            with session as s:
                response = s.get(url, headers=headers, timeout=5, params=params)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:    
            raise  Exception("Connection refused: %s" %e)

    def _handle_response(slef,response):
        '''Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        '''
        if not str(response.status_code).startswith('2'):
            raise BinanceAPIException(response)
        try:
            return response.json()
        except ValueError:
            raise BinanceRequestException('Invalid Response: %s' % response.text)
        except Exception as e:
            raise Exception("other Exception: %s" %e)

    def get_attribute(self):
        return self.symbol
    
    def server_time(self):
        url = self.HOST + '/api/v1/time'
        response = requests.get(url)
        return response.json()
        
    def exchange_info(self):
        # Current exchange trading rules and symbol information
        url = self.HOST + '/api/v1/exchangeInfo'
        response = requests.get(url)
        return response.json()
    
    def order_book(self,limit=50):
        #
        PATH = '/api/v1/depth'
        params = {'symbol':self.symbol,
                  'limit':limit}
        return self._get(self.HOST + PATH, params)
    
    def recent_trades(self,limit=50):
        #Get recent trades (up to last 500)
        PATH = '/api/v1/trades'
        params = {'symbol':self.symbol,
                  'limit':limit}
        return self._get(self.HOST + PATH, params)
    
    def older_trades(self,limit=50,fromID=None):
        #Get older trades.
        PATH = '/api/v1/historicalTrades'
        params = {'symbol':self.symbol,
                  'limit':limit}
        if fromID:
            params['formID'] = fromID
        return self._get(self.HOST + PATH, params)
        
    def aggregate_trades(self,**kwargs):
        '''
        Get compressed, aggregate trades. 
        Trades that fill at the time, from the same order, with the same price
        will have the quantity aggregated.
        
        ：kwargs formID: LONG, ID to get aggregate trades from INCLUSIVE.
        ：kwargs startTime: LONG,Timestamp in ms to get aggregate trades from INCLUSIVE.
        ：kwargs endTime: LONG,
        ：kwargs limit: INT, Default 500; max 500.
        '''
        PATH = '/api/v1/aggTrades'
        params = {'symbol':self.symbol}
        params.update(kwargs)
        return self._get(self.HOST + PATH, params)
    
    def kline(self,interval,limit=1,**kwargs):
        '''
        Klines for a symbol, uniquely identified by open time.
        
        :param   interval: ENUM {'1m','3m','5min','15m','30m','1h','1d','1w','1M'}
        :kwargs startTime: LONG,Timestamp in ms.
        :kwargs endTime: LONG,
        '''
        PATH = '/api/v1/klines'
        params = {'symbol':self.symbol,
                  'interval':interval,
                  'limit':limit}
        params.update(kwargs)
        return self._get(self.HOST + PATH, params)
    
    def price_ticker(self):
        #Latest price for a symbol.
        PATH = '/api/v3/ticker/price'
        params = {'symbol':self.symbol}
        return self._get(self.HOST + PATH, params)
        
    def order_book_ticker(self):
        # Best price/qty on the order book for a symbol or symbols.
        PATH = '/api/v3/ticker/bookTicker'
        params = {'symbol':self.symbol}
        return self._get(self.HOST + PATH, params)
    
    def get_all_tickers(self):
        PATH = '/api/v3/ticker/bookTicker'
        return self._get(self.HOST + PATH, {})
