from season import *
import os
import json
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
from matplotlib import animation, rc


def gradient_descent(x, y, m, theta,alpha,verbose=True):
  costs, thetas, preds = [], [] ,[]  #used for plotting
  conv,idx = 1,0
  costs.append(1e10)    
  while conv:
    pred= np.dot(x, theta)   #y_prediction
    preds.append(pred)
    error = pred - y          
    cost = 1/(2*m) * np.dot(error.T, error) 
    if verbose: print(f'here is cost {cost} at iteration {idx}')
    costs.append(cost)
    theta = theta - (alpha * (1/m)) * np.dot(x.T,error)
    thetas.append(theta)
    if costs[idx]-costs[idx+1] < 1e-9:
        conv = 0
    idx+=1
  costs.pop(0)   
  return costs, thetas, preds






