#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 13:59:15 2021
@Brief:
Collection of Functions used for fetching the data pertaining to the stock/ETF
of interest

@author: prasanna
"""
from yahoofinancials import YahooFinancials
from datetime import date, timedelta
import pandas as pd
import numpy as np
import csv

def ISIN2Tic (ISIN, ref_file):
    f_in = open(ref_file, "r")
    reader = csv.reader(f_in)
    for line in reader:
        if line[3] == ISIN:
            return line[7]

def WKN2Tic (WKN, ref_file):
    f_in = open(ref_file, "r")
    reader = csv.reader(f_in)
    for line in reader:
        if line[6] == '000'+WKN:
            return line[7]
        
def Get_RetVol (ticker, period):
    # set date range for historical prices
    end_time = date.today()
    start_time = end_time - timedelta(days=period)
    
    # reformat date range
    end = end_time.strftime('%Y-%m-%d')
    start = start_time.strftime('%Y-%m-%d')
    
    #ticker = ISIN2Tic('LU1602144732')
    
    json_prices = YahooFinancials(ticker).get_historical_price_data(start, end, 'daily')
    prices = pd.DataFrame(json_prices[ticker]['prices'])[['formatted_date', 'close']]
    prices.sort_index(ascending=False, inplace=True)
    ref_tradays = len(prices)
    # To avoid nan, taking two days earlier closing price
    returns = (prices.close[prices.close.size-2] - prices.close[0]) / prices.close[0]
    prices['returns'] = (np.log(prices.close /    prices.close.shift(-1)))
    # calculate daily standard deviation of returns
    daily_std = np.std(prices.returns)
    # annualized daily standard deviation
    volatality = daily_std * ref_tradays ** 0.5
    
    return ref_tradays, returns, volatality
