#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 10:17:47 2021

@author: prasanna
Ref: https://tinytrader.io/how-to-calculate-historical-price-volatility-with-python/
"""
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

import pandas as pd
import stockfetcher as sf

DEBUG = 0
#Names of the ETF/Shares as ISIN code
stock = ['FR0010655712','FR0010688192','FR0010717090','FR0013284304','LU1602144229',
         'LU1602144575','LU1602144732','LU1602144906','LU1681037864','LU1681038243',
         'LU1681038599','LU1681038672','LU1681038912','LU1681039134','LU1681039563',
         'LU1681039647','LU1681040223','LU1681040900','LU1681041031','LU1681041460',
         'LU1681041890','LU1681042609','LU1681043599','LU1681043912','LU1681044480',
         'LU1681044647','LU1681044720','LU1681045024','LU1681045370','LU1681045537',
         'LU1681046931','LU1681047319','LU1681048804','LU1681049109','LU1737652237',
         'LU1737652310','LU1737652583','LU1737652823','LU1737653045','LU1737653714',
         'LU1737653987','LU1737654019','LU1931974262','LU1931974429','LU1931974692',
         'LU1931974775','LU1931974858','LU1931975079','LU1931975152','LU1931975236',
         'LU2037748774','LU1861138961','LU2109787635','LU1861137484','LU1861136247',
         'LU1861134382','LU1806495575','LU1437017863','LU2037748345','LU1861132840',
         'LU1829220216','LU0533033667','LU2197908721','LU0496786574','LU1838002480',
         'FR0007056841','FR0010361683','LU1923627092','LU1812092168','LU1832418773',
         'LU1287022708','LU1900068328','LU1841731745','LU0832436512','LU1900066207',
         'LU2009202107','DE000ETF9033','DE000ETF9082','DE000ETF9074','LU0252633754',
         'LU0603942888','LU1769088581','LU1792117779','LU1563454823','LU1563454310',
         'LU1981859819','FR0010527275','FR0010524777','LU1792117696','DE000ETF7011',
         'LU0488317701','LU0419741177','LU2023678282','LU2023678878','LU2023679090',
         'LU2023679256','LU2023678449','DE000ETF9090','LU2198883410','LU2198882362',
         'LU2195226068','LU2198884491']
'''
stock = ['LU2023679090']
'''

# Get Reference
#Constants
ticker = '^GDAXI'
period = 365 * 3
ref_file="t7-xetr-allTradableInstruments.csv"
ref_tradays, ref_returns, ref_vol = sf.Get_RetVol(ticker, period)

df = pd.DataFrame(columns=['Ticker', 'Returns', 'Volatality', 'Incomplete'])
if (DEBUG):
    print('Ticker:', ticker, 'No of TradingDays:', ref_tradays,
          'returns:', ref_returns*100, 'Vol:', ref_vol*100)

for i in range(0,len(stock)):
    ticker = sf.ISIN2Tic(stock[i], ref_file)+'.DE'
    if (DEBUG):
        print (i, stock[i], ticker)
    try:
        tradays, returns, vol = sf.Get_RetVol(ticker, period)
        if(tradays < ref_tradays-1):           
            incomplete = 'red'
            if (DEBUG):
                print('Error in Ticker:', ticker, 'Delta ref_tradays:',ref_tradays-tradays)
        elif (returns < ref_returns):
            incomplete = 'yellow'
        else:
            incomplete = 'blue'
        if (DEBUG):
            print('Ticker:', ticker, 'returns:', returns*100, 'Vol:', vol*100)
        df = df.append({'Ticker': ticker, 'Returns':returns, 'Volatality':vol,
                        'Incomplete':incomplete}, ignore_index=True)
    except:
        df = df.append({'Ticker': ticker, 'Returns':0.0, 'Volatality':0.0, 
                        'Incomplete': 1}, ignore_index=True)
        print('Exception Ticker:', ticker, 'returns:', 0, 'Vol:', 0.0)
        pass

#Ploting
        
fig = go.Figure(data=go.Scatter(
    x=df.Returns*100,
    y=df.Volatality*100,
    text=df.Ticker,
    marker_color=df.Incomplete,
    name='ETFs/Stocks',
    mode='markers'))

fig.add_trace(go.Scatter(x=[ref_returns*100], y=[ref_vol*100],
                         text='DAX40', name='Reference Index',
                         mode='markers', marker=dict(size=30, color='pink')))
fig.update_layout(title='Risk vs Volatality chart (DKB Aktion ETF analysis)'
                  '<br><sup>Blue: Complete, Yellow: (returns < reference), Red: Data incomplete</sup>',
                  xaxis_title="Returns (%)", yaxis_title="Volatality (%)",)
fig.show()