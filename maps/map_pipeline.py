import os
from branca.element import Template, MacroElement
import sys 
import json
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster
import pandas as pd

def generate_maps(data,start_year,stop_year, verbose=True):
  
  colors = [
    'red',
    'blue',
    'gray',
    'darkred',
    'lightred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray',
    'black'
  ]

  colorss = {} 
  for i, j in enumerate(range(start_year, stop_year)):
    colorss[str(j)] = colors[i]
  
  keys = list(set([data['rows'][i]['dc_dist'] for i in range(len(data['rows']))]))

  for i in range(len(keys)):
   crime = keys[i]
   res = str(start_year)+'_'+str(stop_year)+'_'+crime.replace(' ','_').replace('/','')+'.html'
   if verbose: print(f' Processing Map for {crime}')
   m = folium.Map(location=[39.9526, -75.1652], zoom_start=5)
   marker_cluster = MarkerCluster(disableClusteringAtZoom=20).add_to(m)
   d = {}
   for i in range(len(data['rows'])):
     if data['rows'][i]['dc_dist'] == crime:
       loc = []
       date = data['rows'][i]['dispatch_date_time'].split('T')
       X,Y = data['rows'][i]['point_x'], data['rows'][i]['point_y']
       #if isinstance(type(X), float) and isinstance(type(Y), float):
       try:
         folium.Marker(location=[Y,X],
                      popup=data['rows'][i],
                      icon=folium.Icon(color=colorss[date[0].split('-')[0]],icon='info-sign')).add_to(marker_cluster)
       except Exception: continue
   template = """
    {% macro html(this, kwargs) %}
      <!doctype html>
      <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Philadelphia Gun Violence Visualization</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
        
        <script>
        $( function() {
          $( "#maplegend" ).draggable({
                          start: function (event, ui) {
                              $(this).css({
                                  right: "auto",
                                  top: "auto",
                                  bottom: "auto"
                              });
                          }
                      });
      });

        </script>
      </head>
      <body>

       
      <div id='maplegend' class='maplegend' 
          style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
           border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
           
      <div class='legend-title'>Color Map</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
          <li><span style='background:red;opacity:0.7;'></span>2006</li>
          <li><span style='background:blue;opacity:0.7;'></span>2007</li>
          <li><span style='background:darkred;opacity:0.7;'></span>2008</li>
          <li><span style='background:orange;opacity:0.7;'></span>2009</li>
          <li><span style='background:beige;opacity:0.7;'></span>2010</li>
          <li><span style='background:green;opacity:0.7;'></span>2011</li>
          <li><span style='background:darkgreen;opacity:0.7;'></span>2012</li>
          <li><span style='background:lightgreen;opacity:0.7;'></span>2013</li>
          <li><span style='background:darkblue;opacity:0.7;'></span>2014</li>
          <li><span style='background:lightblue;opacity:0.7;'></span>2015</li>
          <li><span style='background:purple;opacity:0.7;'></span>2017</li>
          <li><span style='background:darkpurple;opacity:0.7;'></span>2018</li>
          <li><span style='background:pink;opacity:0.7;'></span>2019</li>
          <li><span style='background:cadetblue;opacity:0.7;'></span>2020</li>
          <li><span style='background:lightgrey;opacity:0.7;'></span>2021</li>
          <li><span style='background:black;opacity:0.7;'></span>2022</li>
        </ul>
      </div>
      </div>
       
      </body>
      </html>

      <style type='text/css'>
        .maplegend .legend-title {
          text-align: left;
          margin-bottom: 5px;
          font-weight: bold;
          font-size: 40%;
          }
        .maplegend .legend-scale ul {
          margin: 0;
          margin-bottom: 5px;
          padding: 0;
          float: left;
          list-style: none;
          }
        .maplegend .legend-scale ul li {
          font-size: 40%;
          list-style: none;
          margin-left: 0;
          line-height: 18px;
          margin-bottom: 2px;
          }
        .maplegend ul.legend-labels li span {
          display: block;
          float: left;
          height: 16px;
          width: 30px;
          margin-right: 5px;
          margin-left: 0;
          border: 1px solid #999;
          }
        .maplegend .legend-source {
          font-size: 40%;
          color: #777;
          clear: both;
          }
        .maplegend a {
          color: #777;
          }
      </style>
      {% endmacro %}"""
   macro = MacroElement()
   macro._template = Template(template)
   m.get_root().add_child(macro)
   print(f'saving map {res}')
   m.save(res)
 






