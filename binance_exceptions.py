# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 13:08:29 2017

@author: Zeyu
"""

class BinanceAPIException(Exception):
    
    def __init__(self,response):
        json_res = response.json()
        self.status_code= response.status_code
        self.message = json_res['msg']
        self.code = json_res['code']
    
    def __str__(self):
        return 'API Error(code=%s): %s' % (self.code,self.message)


class BinanceRequestException(Exception):
    def __init__(self,message):
        self.message = message
    
    def __str__(self):
        return 'BinanceRequestException: %s' % self.message
        
        
        
        
    
    