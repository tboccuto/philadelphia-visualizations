#!/usr/bin/env python3
import os
from branca.element import Template, MacroElement
import sys 
import json
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster

def plot_markers(data):
  li = sorted([i for i in data if i[-8:] == '.geojson'])
  points = {}
  for u in range(len(li)):
    points[u] = []
    with open(li[u]) as f:
      d = json.load(f)
      try:
        for ii in range(len(d['features'])):
          coords = d['features'][ii]['geometry']['coordinates'][::-1]
          properties = d['features'][ii]['properties']
          points[u].append([properties, coords])
      except Exception: continue

  m = folium.Map(location=[39.9526, -75.1652], zoom_start=5)
  colorss = ["red", "blue", 'green', 'purple', 'orange', 'pink', 
             'white', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 
             'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 
             'gray', 'black', 'lightgray']
  marker_cluster = MarkerCluster(disableClusteringAtZoom=20).add_to(m) 

  dat = 0
  while dat < len(points):
    for j in range(len(points[dat])):
      folium.Marker(points[dat][j][1],
            popup=points[dat][j][0],
            icon=folium.Icon(color=colorss[dat], icon='info-sign')
            ).add_to(marker_cluster)
    dat += 1
    print(f'iteration: {dat}') 
  
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
      <li><span style='background:red;opacity:0.7;'></span>2015</li>
      <li><span style='background:blue;opacity:0.7;'></span>2016</li>
      <li><span style='background:green;opacity:0.7;'></span>2017</li>
      <li><span style='background:purple;opacity:0.7;'></span>2018</li>
      <li><span style='background:orange;opacity:0.7;'></span>2019</li>
      <li><span style='background:pink;opacity:0.7;'></span>2020</li>
      <li><span style='background:white;opacity:0.7;'></span>2021</li>
      <li><span style='background:beige;opacity:0.7;'></span>2022</li>

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
  m.save('philly_shootings.html')

plot_markers([i for i in os.listdir()])



