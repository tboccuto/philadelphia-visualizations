#!/usr/bin/env python3
import os
import json
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib as mpl
from scipy import signal
import matplotlib.pyplot as plt   
from collections import Counter
from statsmodels.tsa.seasonal import seasonal_decompose

#ignore homicides,do that seperate
def plot_all_dispatch_crimes(data):
  AD = [data['rows'][i]['dc_dist'] for i in range(len(data['rows']))]
  ADC = Counter(ADC)
  dat = [[k, v] for k,v in all_crime_counts.items() if k != 'Homicide - Criminal ' and k != 'Homicide - Criminal']
  df = pd.DataFrame(dat)
  fig = px.bar(df, x=[i[1] for i in dat], y=[i[0] for i in dat], title="Crime Dispatches in Philadelphia from 2006 - 2022")
  return fig

def plot_year_dispatch(y, data):
  for i in range(1, len(data['rows'])):
    d2['rows'][i]['dispatch_date_time'] = d2['rows'][i]['dispatch_date_time'].split('T')
  cdispatch = [d2['rows'][i] for i in range(len(data['rows'])) if y in d2['rows'][i]['dispatch_date_time'][0]]
  ydispatch_count = Counter([cdispatch[i]['dc_dist'] for i in range(len(cdispatch))])
  dat = [[k, v] for k,v in ydispatch_count.items()]
  df = pd.DataFrame(dat)
  fig = px.bar(df, x=[i[1] for i in dat2], y=[i[0] for i in dat2], title="Crime Dispatches in Philadelphia year "+str(y))
  return fig

def init_season(data, crime):
  s = {}
  for i in range(1, len(data['rows'])):
    year, month, _ = data['rows'][i]['dispatch_date_time'][0].split('-')
    s[year+'-'+month] = 0
  for k in s.keys():
    c = 0
    for j in range(1, len(data['rows'])):
      if crime in data['rows'][i]['dc_dist'] and k in data['rows'][i]['dispatch_date_time'][0]:
        c += 1
    s[k] = c
  return list(sorted(s.items()))

def init_seasons(data, crimes):
  g = {}
  for c in crimes:
    g[crimes] = init_season(data,c)
  return g

def plot_simple_time_series(df, x, y, title="", xlabel='time', ylabel='# of instances of crime', dpi=100):
  plt.figure(figsize=(15,4), dpi=dpi)
  plt.plot(x, y, color='tab:red')
  plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
  plt.show()

def plot_two_sided_simple_time_series(crime,df, x, y, title="", xlabel='time', ylabel='# of instances of crime', dpi=100):
  x = df[0].values
  y1 = df[1].values
  fig, ax = plt.subplots(1, 1, figsize=(20,5), dpi= 120)
  plt.fill_between(x, y1=y1, y2=-y1, alpha=0.5, linewidth=2, color='seagreen')
  plt.ylim(-6500, 6500)
  plt.title('{} (Two Side View)'.format(crime), fontsize=16)
  plt.hlines(y=0, xmin=np.min(df[0]), xmax=np.max(df[0]), linewidth=.5)
  plt.show()

def mean_variance(X):
  X = np.log(X)
  half = X // 2
  X1, X2 = X[0:half], X[half:]
  M1, M2 = X1.mean(), X2.mean()
  V1, V2 = X1.var(), X2.var()
  ADF = adfuller(X)
  return [M1, M2, V1, V2]

#data should be dataframe, d[0]: time d[1]: values
def detrend_best_fit(data):
  return signal.detrend(data[1].values)

#data should be dataframe, d[0]: time d[1]: values 
def multiplicative_decomposition_detrending(data, multiplicative_decomposition):
  return np.array(df[1].values, dtype=np.float32) - np.array(multiplicative_decomposition.trend, dtype=np.float32)





