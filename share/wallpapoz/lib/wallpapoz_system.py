#================================================
#
#    wallpapoz_system.py - Wallpapoz
#    Copyright (C) 2007 Vajrasky Akbar Kok <arjuna@vajrasky.net>
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

class WallpapozSystem:

  def __init__(self):
    self.finding_screen_resolution()
    self.finding_total_workspaces()
    self.finding_desktop_environment()

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

  ## class method to find which desktop environment user uses
  def finding_desktop_environment(self):
    raw_window_id = os.popen('xprop -root _NET_SUPPORTING_WM_CHECK').read()
    window_id = raw_window_id[46:raw_window_id.find("\n")]
    raw_wm_name = os.popen('xprop -id ' + window_id + ' 8s _NET_WM_NAME').read()
    wm_name = raw_wm_name[29:raw_wm_name.rfind('"')]
    # default is Gnome3.
    self.window_manager = 'Gnome3'
    if wm_name=='Xfwm4':
      self.window_manager = 'XFCE4'
    elif wm_name=='Fluxbox':
      self.window_manager = 'Fluxbox'
    elif wm_name=='Marco' or wm_name=='Metacity (Marco)':
      self.window_manager = 'MATE'
    elif wm_name=='Mutter (Muffin)':
      self.window_manager = 'CINNAMON'
    elif wm_name=='Mutter(Budgie)':
      self.window_manager = 'Gnome3'
    else:
      output = os.popen("gnome-session --version")
      result = output.readlines()
      version = result[0].split()[1].split('.')[0]
      if version == '2':
        self.window_manager = 'Gnome'
      elif version == '3':
        self.window_manager = 'Gnome3'

  ## class method to find amount of workspaces in user desktop
  def finding_total_workspaces(self):
    try:
      self.total_workspaces = int(os.popen("xprop -root _NET_NUMBER_OF_DESKTOPS").read()[36:38])
    except:
      self.total_workspaces = 1
      
  ## class method to find how many rows and columns of workspaces
  def finding_row_and_column(self):
    self.row_workspaces = self.geometry_height / self.screen_height
    self.column_workspaces = self.geometry_width / self.screen_width

  ## class method to find how many workspaces there are in user desktop
  def get_total_workspaces(self):
    return self.total_workspaces

  ## class method to know what workspace we are in now
  def current_desktop(self):
    raw_workspace = os.popen('xprop -root _NET_CURRENT_DESKTOP').read()
    workspace = int(raw_workspace[33] + raw_workspace[34])
    return workspace

  ## class method to change desktop wallpaper
  def change_wallpaper(self, wallpaper):
    if self.window_manager == "Gnome":
      os.system('gconftool-2 -t string -s /desktop/gnome/background/picture_filename ' +
        '"' + wallpaper + '"' + ' -s /desktop/gnome/background/picture_options ' +
        self.wallpaper_style)
    elif self.window_manager == "Gnome3":
      os.system("gsettings set org.gnome.desktop.background picture-uri 'file://" + wallpaper + "'")
      os.system("gsettings set org.gnome.desktop.background picture-options " + self.wallpaper_style)
    elif self.window_manager == "MATE":
      os.system('gsettings set org.mate.background picture-filename ' + wallpaper)
      os.system('gsettings set org.mate.background picture-options ' + self.wallpaper_style)
    elif self.window_manager == "CINNAMON":
      os.system("gsettings set org.cinnamon.desktop.background picture-uri 'file://" + wallpaper + "'")
      os.system("gsettings set org.cinnamon.desktop.background picture-options " + self.wallpaper_style)
    elif self.window_manager == "XFCE4":
      os.system("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s " +
        '"' + wallpaper + '"')
      os.system("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-style -s " +
        self.wallpaper_style)
    elif self.window_manager == "Fluxbox":
      os.system("feh " + self.wallpaper_style + " " + wallpaper)

  ## class method to find current desktop wallpaper
  def finding_current_wallpaper(self):
    if self.window_manager == "Gnome":
      return os.popen("gconftool-2 -g /desktop/gnome/background/picture_filename").read()[:-1]
    elif self.window_manager == "Gnome3":
      return os.popen("gsettings get org.gnome.desktop.background picture-uri").read()[8:-2]
    elif self.window_manager == "MATE":
      return os.popen("gsettings get org.mate.background picture-filename").read()[:-1]
    elif self.window_manager == "CINNAMON":
      return os.popen("gsettings get org.cinnamon.desktop.background picture-uri").read()[8:-2]
    elif self.window_manager == "XFCE4":
      return os.popen("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path").read()[:-1]
    elif self.window_manager == "Fluxbox":
      home = os.environ['HOME']
      try:
        with open(home + '/.fehbg') as feh_setting_file:
          feh_setting_file_content = feh_setting_file.read()
          return feh_setting_file_content[15:feh_setting_file_content.find("'", 15)]
      except IOError as e:
        return ''
    else:
      return ''

  ## class method to detect that we have changed workspace or not
  def has_changed(self, previous_desktop, cur_desk):
    if previous_desktop != cur_desk:
      # if we move to workspace that we don't use, just ignore
      if cur_desk >= self.total_workspaces:
        return False
      return True
    else:
      return False
