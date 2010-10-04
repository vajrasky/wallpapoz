#================================================
#
#    wallpapoz_system.py - Wallpapoz 
#    Copyright (C) 2007 Akbar <akbarhome@gmail.com>
#
#================================================
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#================================================

## wallpapoz_system.py -- finds current desktop and changes wallpaper
# achieve goal by calling external program

import os
import string

class WallpapozSystem:

  def __init__(self):
    self.wallpaper_style = 'scaled'
    self.finding_screen_resolution()
    self.check_beryl()
    if self.beryl:
      self.finding_row_and_column()
    self.finding_total_workspaces()

  def set_style(self, style):
    self.wallpaper_style = style

  ## class method to find monitor resolution
  def finding_screen_resolution(self):
    raw_resolution = os.popen('xwininfo -root').read()
    start_width = raw_resolution.find('Width')
    end_width = raw_resolution.find('\n',start_width)
    start_height = raw_resolution.find('Height')
    end_height = raw_resolution.find('\n', start_height)
    self.screen_width = int(raw_resolution[start_width+7:end_width])
    self.screen_height = int(raw_resolution[start_height+8:end_height])

  ## class method to find amount of workspaces in user desktop
  def finding_total_workspaces(self):
    if self.beryl:
      self.total_workspaces = self.row_workspaces * self.column_workspaces
    else:
      self.total_workspaces = int(os.popen("xprop -root _NET_NUMBER_OF_DESKTOPS").read()[36:38])

  ## class method to find if user use beryl in his system or not
  def check_beryl(self):
    raw_geometry = os.popen('xprop -root _NET_DESKTOP_GEOMETRY').read()
    # output of xprop -root _NET_DESKTOP_GEOMETRY is '_NET_DESKTOP_GEOMETRY(CARDINAL) = 1024, 768\n'
    # and we just need the '1024, 768' part
    raw_geometry = raw_geometry[34:raw_geometry.find('\n')]
    geometry = string.split(raw_geometry, ', ')
    self.geometry_width = int(geometry[0])
    self.geometry_height = int(geometry[1])
    self.beryl = False
    if self.geometry_width!=self.screen_width:
      self.beryl = True
      return
    if self.geometry_height!=self.screen_height:
      self.beryl = True

  ## class method to find how many rows and columns of workspaces
  def finding_row_and_column(self):
    self.row_workspaces = self.geometry_height / self.screen_height
    self.column_workspaces = self.geometry_width / self.screen_width

  ## class method to find how many workspaces there are in user desktop
  def get_total_workspaces(self):
    return self.total_workspaces

  ## class method to know what workspace we are in now
  def current_desktop(self):
    if self.beryl:
      raw_viewport = os.popen('xprop -root _NET_DESKTOP_VIEWPORT').read()
      # output of xprop -root _NET_DESKTOP_VIEWPORT is '_NET_DESKTOP_VIEWPORT(CARDINAL) = 1024, 768\n'
      # and we just need the '1024, 768' part
      raw_viewport = raw_viewport[34:raw_viewport.find('\n')]
      viewport = string.split(raw_viewport, ', ')
      x_pos = int(viewport[0]) / self.screen_width
      y_pos = int(viewport[1]) / self.screen_height
      workspace = x_pos + self.column_workspaces * y_pos
    else:
      raw_workspace = os.popen('xprop -root _NET_CURRENT_DESKTOP').read()
      workspace = int(raw_workspace[33] + raw_workspace[34])
    return workspace

  ## class method to change desktop wallpaper
  def change_wallpaper(self, wallpaper):
    os.system('gconftool-2 -t string -s /desktop/gnome/background/picture_filename ' + 
	'"' + wallpaper + '"' + ' -s /desktop/gnome/background/picture_options ' + 
	self.wallpaper_style)

  ## class method to detect that we have changed workspace or not
  def has_changed(self, previous_desktop, cur_desk):
    if previous_desktop != cur_desk:
      # if we move to workspace that we don't use, just ignore
      if cur_desk >= self.total_workspaces:
	return False
      return True
    else:
      return False
