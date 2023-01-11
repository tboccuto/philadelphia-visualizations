import numpy as np

class LinearRegression:
  def __init__(self, X, y, plotting=True):
    self.X = X
    self.y = y
    self.preds = []
    self.costs = []
    self.thetas = []
    self.rtheta = []
    self.cost = None

  def feature_scaling(self, X, Y):
    return (X - X.mean())/X.std(), (Y - Y.mean())/Y.std()

  def gradient_descent(self, x, y, theta,alpha,fs=True,verbose=False):
    if fs:
      x, y = self.feature_scaling(x, y)
    if len(x.shape) == 1:
      x = np.c_[np.ones(x.shape[0]),x]
    self.X = x #update attr
    conv,idx = 1,0
    self.costs.append(1e10)
    while conv:
      self.preds.append(np.dot(x, theta)) #y_prediction
      error = self.preds[idx] - y
      self.costs.append(1/(2*y.size) * np.dot(error.T, error))
      theta = theta - (alpha * (1/y.size)) * np.dot(x.T,error)
      self.thetas.append(theta)
      if verbose: print(f'{idx}[cost:{self.costs[idx]} preds: {self.preds[idx]} thetas: {self.thetas[idx]}]')
      if self.costs[idx]-self.costs[idx+1] < 1e-9:
          conv = 0
      idx+=1
    self.costs.pop(0)
    self.rtheta.append([theta[0], theta[1]])
    self.cost = self.costs[-1]
    if verbose: print(f'Metrics {self.rtheta} {self.cost}')







