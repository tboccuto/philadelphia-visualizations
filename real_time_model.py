import os
import sys
import json
import urllib.request
from matplotlib.axis import XAxis, YAxis import numpy as np import pandas as pd from d import month_count, month_counts import seaborn as sns
import plotly.express as px
from scipy import signal
import matplotlib.pyplot as plt   
from matplotlib import animation, rc
from collections import Counter
from statsmodels.tsa.seasonal import seasonal_decompose
from season import *
from map_pipeline import *
from linear_regression import *

class RealTimeModel:
  def __init__(self, path):
    """
    Constructor
    Parameters
    ----------
    path: string
          sysarv data
    
    query SQL for new batch
    and update class attributes
    """
    self.path = path
    self.data = None
    self.all_crime_counts = None
    self.keys = None
    self.stacked_dfs = None
    with urllib.request.urlopen(self.path.replace(' ', '%20')) as url:
      self.data = json.load(url)
      
    self.all_crime_counts = Counter([self.data['rows'][i]['dc_dist'] for i in range(len(self.data['rows']))])
    self.keys = list(self.all_crime_counts.keys())
    self.stacked_dfs = stack_df(self.data)


    print(f'Num of categories {len(self.keys)}')
    
  def display_all_dispatch_counts_plotly(self, data, year=None):
    """
    Writes Png of horizontal line graph for counts of crimes
    Parameters
    ----------
    data: json object
    """
    dat = None
    if not year:
      dat = [[k, v] for k,v in self.all_crime_counts.items() if k != 'Homicide - Criminal ' and k != 'Homicide - Criminal']
      df = pd.DataFrame(dat)
      title = 'Crime Dispatches in Philadelphia from 2006 - 2022'
    else:
      for i in range(1, len(data['rows'])):
        self.data['rows'][i]['dispatch_date_time'] = self.data['rows'][i]['dispatch_date_time'].split('T')
      cdispatch = [self.data['rows'][i] for i in range(len(data['rows'])) if year in self.data['rows'][i]['dispatch_date_time'][0]]
      year_crimes_counts = Counter([cdispatch[i]['dc_dist'] for i in range(len(cdispatch))])
      dat = [[k, v] for k,v in year_crimes_counts.items() if k != 'Homicide - Criminal ' and k != 'Homicide - Criminal']
      df = pd.DataFrame(dat)
      title = 'Crime Dispatches in Philadelphia year ' + str(year)
    fig = px.bar(df, x=[i[1] for i in dat], y=[i[0] for i in dat], title=title)
    fig.write_image('display_all_dispatch_counts-plotly.png')

  def plot_df_line_graph(self):
    """
    Generate line graph, 
    Make new dir, 
    Save all png to new dir
    """
    for i in range(len(self.stacked_dfs)):
      title = self.stacked_dfs[i].columns[1]
      title = title.replace('/','').replace('-','').replace(' ','')
      plot = self.stacked_dfs[i].plot(x='dates', y=li[i].columns[1])
      fig = plot.get_figure()
      new_dir = os.getcwd()+'/line_graphs'
      if not os.path.exists(new_dir): os.makedirs(new_dir)
      fig.savefig(new_dir+'/'+title+'.png')

  def plot_line_graph_doublesided(self):
    """
    Generate double sided line graph,
    Make new dir,
    Save all png to new dir
    """
    for i in range(len(self.stacked_dfs)):
      title = self.stacked_dfs[i].columns[1]
      title = title.replace('/','').replace('-','').replace(' ','')
      x, y1 = self.stacked_dfs[i]['dates'].values, self.stacked_dfs[i][self.stacked_dfs[i].columns[1]].values
      fig, ax = plt.subplots(1, 1, figsize=(20,5), dpi= 120)
      plt.fill_between(x, y1=y1, y2=-y1, alpha=0.5, linewidth=2, color='seagreen')
      plt.ylim(-6500, 6500)
      plt.title(title+' (Two Side View)', fontsize=16)
      plt.hlines(y=0, xmin=np.min(x), xmax=np.max(x), linewidth=.5)
      #f = fig.get_figure()
      new_dir = os.getcwd()+'/two_sided_graphs'
      if not os.path.exists(new_dir): os.makedirs(new_dir)
      fig.savefig(new_dir+'/'+title+'.png')

  def plot_add_decomposition(self):
    """
    Generate Additive Deocomposition graphs
    Make new dir,
    Save all png to new dir 
    """
    for i in range(len(self.stacked_dfs)):
      title = self.stacked_dfs[i].columns[1]
      title = title.replace('/','').replace('-','').replace(' ','')
      add_decomp = seasonal_decompose(self.stacked_dfs[i][self.stacked_dfs[i].columns[1]].values, model='additive', period=30)
      plot = additive_decomposition.plot().suptitle(title +' Additive Decomposition', fontsize=16)
      plt.tight_layout(rect=[0, 0.03, 1, 0.95])
      fig = plot.get_figure()
      new_dir = os.getcwd()+'/additive_decomposition'
      if not os.path.exists(new_dir): os.makedirs(new_dir)
      fig.savefig(new_dir+'/'+title+'.png')

  def plot_mult_decomposition(self):
    """
    Generate Additive Deocomposition graphs
    Make new dir,
    Save all png to new dir 
    """
    for i in range(len(self.stacked_dfs)):
      title = self.stacked_dfs[i].columns[1]
      title = title.replace('/','').replace('-','').replace(' ','')
      add_decomp = seasonal_decompose(self.stacked_dfs[i][self.stacked_dfs[i].columns[1]].values, model='multiplicative', period=30)
      plot = additive_decomposition.plot().suptitle(title +' Additive Decomposition', fontsize=16)
      plt.tight_layout(rect=[0, 0.03, 1, 0.95])
      fig = plot.get_figure()
      new_dir = os.getcwd()+'/additive_decomposition'
      if not os.path.exists(new_dir): os.makedirs(new_dir)
      fig.savefig(new_dir+'/'+title+'.png')

  def plot_linear_regression_line_plot(self):
    """
    Use library to calc Linear Regression
    Make new dir,
    Save all png to new dir
    """
    for i in range(len(self.stacked_dfs)):
      title =self.stacked_dfs[i].columns[1]
      title = title.replace('/','').replace('-','').replace(' ','')
      parsed_df = parse_dataframe(self.stacked_dfs[i], self.stacked_dfs[i].columns[1])
      fig = sns.lmplot(data=parsed_df, x=parsed_df.columns[0], y=parsed_df.columns[1] ,aspect=2, height=10)
      fig.add_legend()
      new_dir = os.getcwd()+'/LG_plots'
      if not os.path.exists(new_dir): os.makedirs(new_dir)
      fig.savefig(new_dir+'/'+title+'.png')

  def plot_correlation_matrices(self):
    """
    Generate correlation matrices between Dates and Crimes
    Make new Dir
    Save all png to new dir
    """
    for i in range(len(self.stacked_dfs)):
      title =self.stacked_dfs[i].columns[1]
      title = title.replace('/','').replace('-','').replace(' ','')
      parsed_df = parse_dataframe(self.stacked_dfs[i], self.stacked_dfs[i].columns[1])
      plt.figure(figsize=(12, 6))
      plot = sns.heatmap(parsed_df.corr(), annot=True, cmap="Wistia")
      new_dir = os.getcwd()+'/correlaton_matrices'
      if not os.path.exists(new_dir): os.makedirs(new_dir)
      fig = plot.get_figure()
      fig.savefig(new_dir+'/'+title+'.png')

  def plot_distributions(self):
    pass
    







  def plot_monthly_crime_trends(self, doublesided=True, ndecomp=True, lg_line=True, correlation_matrix=True, \
                                distplot=True, verbose=True):
    """
    Generate monthly plots of crimes across time
    opt to do double sided plot to see trend more
    opt to seaonal decompostion
    opt for linear regression
    opt for correlation matrix
    opt for distribution plot
    """
    li = []
    for k in self.keys:
      normk = k.replace('/','').strip().replace(' - ','').replace(' ','')
      XAxis,YAxis= 'Months', 'Crime Counts ' + normk
      if verbose: print(f' Crime {k} being processed')
      dat = month_count(self.data, k, sort=True)
      df = pd.DataFrame(dat, columns=['dates', k])
      X, Y = df[0].values, df[1].values
      plt.figure(figsize=(15,4), dpi=dpi)
      plt.plot(X, Y, color='tab:blue')
      plt.gca().set(title="Crime Counts from 2006 to present for theft"+str(normk), xlabel=XAxis, ylabel=YAxis)
      plt.savefig(normk+'_matplot.png')
      if doublesided:
        x = df[0].values
        y1 = df[1].values
        fig, ax = plt.subplots(1, 1, figsize=(20,5), dpi= 120)
        plt.fill_between(x, y1=y1, y2=-y1, alpha=0.5, linewidth=2, color='seagreen')
        plt.ylim(-6500, 6500)
        plt.title(normk + ' (Two Side View)', fontsize=16)
        plt.hlines(y=0, xmin=np.min(df[0]), xmax=np.max(df[0]), linewidth=.5)
        plt.savefig(normk +'_matplot2sided.png')
      if ndecomp:
        mult_decomposition = seasonal_decompose(df[1], model='multiplicative', period=30)
        add_decomposition = seasonal_decompose(df[1], model='additive', period=30)
        plt.rcParams.update({'figure.figsize': (16,12)})
        mult_decomposition.plot().suptitle('Multiplicative Decomposition', fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        add_decomposition.plot().suptitle('Additive Decomposition', fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(normk+'_decomposition_matplot.png')
      if lg_line or correlation_matrix:
       int_dates_df = parse_dataframe(df, k) 

      if lg_line:
        LG_plot = sns.lmplot(data=int_dates_df, x=XAxis, y=YAxis,aspect=2, height=10)
        fig = LG_plot.get_figure()
        fig.savefig('LG'+normk+'.png') 
      if correlation_matrix:
        correlation_matrix_plot = sns.heatmap(int_dates_df.corr(), annot=True, cmap="Wistia")
        correlation_matrix_plot.get_figure()
        fig.savefig('correlation_matrix'+normk+'.png')
      if distplot:
        distplot_log10 = sns.distplot(np.log10(int_dates_df ,bins=len(int_dates_df['dates'])-10,color='b',ax=ax))
        fig = distplot_log10.get_figure()
        fig.savefig('distplot'+'_'+normk+'.png')
 
  def create_crime_maps(self, start, stop):
    """
    See map_pipeline.py for more info
    Using Folium API,
    Specify time step:
    for each year, crime category
      create a map with colorbar
      each instance of crime, plot with color
    """
    generate_maps(self.data, start, stop)

  def linear_regression_animation(self):
    """
    See linear_regression.py for linear
    regression implementation
    
    Perform Multivariate linear Regression on monthly crime counts
    and save fig of the cost and estimation of coeff M 
    """
    li = stack_df(self.data)
    alpha = 0.0001
    theta = np.random.rand(2)
    def init():
      line1.set_data([], [])
      line2.set_data([], [])
      return (line1, line2,)

    # animation function. 
    def animate(i):
      line1.set_data(x[:,1], prediction_list_mod[i])
      line2.set_data(x_mod[:i],cost_list_mod[:i])
      line3.set_data(x_mod[i],cost_list_mod[i])
      annotation1.set_text('J = %.2f' % (cost_list_mod[i]))
      annotation2.set_text('J = %.2f' % (cost_list_mod[i]))
      return line1, line2, line3, annotation1, annotation2

    for i in range(len(li)):
      keys = li[i].columns
      LG = LinearRegression(li[i][keys[0]], li[i][keys[1]])
      gd = LG.gradient_descent(LG.X, LG.y, theta, alpha)
      x, y = LG.X, LG.y ##update shape of x to plot
      ### Animation code
      fname = str([keys[1]]).replace('/','').strip().replace(' - ','').replace(' ','').replace('[', '').replace(']','')
      cost_list = LG.costs
      prediction_list= LG.preds
      xl = np.linspace(0, len(cost_list),len(cost_list))
      cost_list_mod = cost_list[::-1][0::100][::-1]
      x_mod = xl[::-1][0::100][::-1]
      prediction_list_mod = prediction_list[::-1][0::100][::-1]
      print(xl.shape)
      print(len(prediction_list_mod))
      fig = plt.figure(figsize=(12,10))
      ax1=plt.subplot(121)
      ax1.scatter(x[:,1], y, color='C1')
      ax1.set_xlabel('Feature Scaled average number of'+fname+'per month')
      ax1.set_ylabel('Feature Scaled dates')
      ax2=plt.subplot(122)
      ax2.set_xlim(-2,140000)
      ax2.set_ylim((0, 1))
      ax2.set_xlabel('Number of iterations')
      ax2.set_ylabel('Cost Function')
      line1, = ax1.plot([], [], lw=2, visible=True);
      line2, = ax2.plot([], [], lw=2);
      line3, = ax2.plot([], [], 'o');
      annotation1 = ax1.text(-3.5, 3, '', size=18)
      annotation2 = ax2.text(16500, .957, '', size=18)
      annotation1.set_animated(True)
      annotation2.set_animated(True)
      #plt.title('Linear Regression on ' ,fname)
      plt.close()
      anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=len(x),interval=15,  blit=True)
      
      #fname = str(li[i][keys[1]]).replace('/','').strip().replace(' - ','').replace(' ','')
      anim.save('LG'+fname+'.gif', writer='imagemagick', fps = 30)




