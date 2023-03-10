#!/usr/bin/env python3
import os
import json
import time
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib as mpl
from scipy import signal
import matplotlib.pyplot as plt   
from collections import Counter
from statsmodels.tsa.seasonal import seasonal_decompose

#TODO: This can be faster
def month_count(data, crime, _sort=False, int_dates=True, verbose=False):
  s, ret = {}, None
  for i in range(1, len(data['rows'])):
    year, month, _ = data['rows'][i]['dispatch_date_time'].split('-')
    s[year+'-'+month] = 0
  for k in s.keys():
    c = 0
    for j in range(1, len(data['rows'])):
      if crime in data['rows'][j]['dc_dist'] and k in data['rows'][j]['dispatch_date_time']:
        c += 1
      if verbose: print(f'k {k}:c {c}')
      s[k] = c
  if _sort:
    s = list(sorted(s.items()))
  if int_dates and isinstance(s, list):
    s = [[int(s[i][0].replace('-','')),s[i][1]] for i in range(len(s))]
  return s

def month_counts(data, crimes):
  g = {}
  for c in crimes:
    g[crimes] = month_count(data,c, _sort=True, verbose=False)
  return g

def stack_df(data, verbose=True):
  d = []
  keys = list(set([data['rows'][i]['dc_dist'] for i in range(len(data['rows']))]))
  for k in keys:
    start = time.time()
    print(f'stacking crime {k}')
    dat = month_count(data, k, _sort=True)
    df = pd.DataFrame(dat, columns=['dates', k])
    d.append(df)
    end = time.time()
    print(f'Time stacking {k} {end - start}')
  return d


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
  return [M1, M2, V1, V2]

#data should be dataframe, d[0]: time d[1]: values
def detrend_best_fit(data):
  return signal.detrend(data[1].values)

#data should be dataframe, d[0]: time d[1]: values 
def multiplicative_decomposition_detrending(data, multiplicative_decomposition):
  return np.array(df[1].values, dtype=np.float32) - np.array(multiplicative_decomposition.trend, dtype=np.float32)

#sns dataframe, crime:str
def parse_dataframe(df, crime, verbose=True):
  cl = {}
  for i in range(len(df['dates'].values)):
    year, month = df['dates'][i].split('-')
    dd = year+month
    cl[int(dd)] = df[df.columns[1]].values[i]
  return pd.DataFrame({'dates':list(cl.keys()),str(crime):list(cl.values())})


