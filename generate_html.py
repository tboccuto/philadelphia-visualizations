#!/usr/bin/env python3
import os

def write_animation_html(verbose=False):
  ret = ""
  entries = os.listdir('LG_gifs/')
  f = open('animations.html','w')
  ret += '<div class="container">'
  for anim in entries:
    ret += '\t'
    ret += '<div class="row">'
    ret += '<img src="{}">'.format('LG_gifs/'+anim)
    ret += '</div>'
  f.write(ret)

  if verbose: print(ret) 

#write_animation_html(0)



