#================================================
#
#    xml_processing.py - Wallpapoz 
#    Copyright (C) 2007 Vajrasky Akbar Kok <akbarhome@gmail.com>
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

## xml_processing.py -- manipulates xml file for gui or daemon

from xml.dom import minidom
import xml
import os
import sys
import gettext
import gtk
from wallpapoz_system import WallpapozSystem

# i18n
APP = "wallpapoz"
DIR = "../../locale"
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
gtk.glade.bindtextdomain(APP, DIR)
gtk.glade.textdomain(APP)
_ = gettext.gettext

## XMLProcessing -- class for processing wallpapoz xml file
class XMLProcessing:

  ## The constructor
  def __init__(self):
    # our document instance
    self.xmldoc = None

    # the configuration file
    home = os.environ['HOME']
    self.config_file = home + "/.wallpapoz/wallpapoz.xml"

    # if wallpapoz run for the first time ( no configuration file )
    # we make default list, for every workspace, we give one wallpaper that is our current wallpaper
    if not os.path.exists(self.config_file):
      print _("No configuration file. Use default configuration.")
      home = os.environ['HOME']
      if not os.path.exists(home + '/.wallpapoz'):
        os.makedirs(home + '/.wallpapoz')

      self.create_configuration_file(self.default_fill_list("treestore"), "treestore")

    # okay, parse the xml file
    try:
      self.xmldoc = minidom.parse(self.config_file)
    except xml.parsers.expat.ExpatError:
      print _("The configuration file is corrupted. Remove it then create a new one again with Wallpapoz!")
      sys.exit()

    # wallpapoz node
    self.wallpapoz_node = self.xmldoc.childNodes[1]

    # wallpapoz type ( workspace or desktop )
    try:
      self.wallpapoz_type = self.wallpapoz_node.attributes["type"].value
    except KeyError:
      self.wallpapoz_type = "workspace"

    # wallpapoz window manager ( gnome, xfce, or fluxbox )
    try:
      self.wallpapoz_window_manager = self.wallpapoz_node.attributes["window"].value
    except KeyError:
      self.wallpapoz_window_manager = "gnome"

    # how many workspace do we have
    wallpapoz_system = WallpapozSystem(self.wallpapoz_window_manager)
    self.workspace_num = wallpapoz_system.get_total_workspaces()

    # our current wallpaper
    self.current_wallpaper = wallpapoz_system.finding_current_wallpaper()
    if self.current_wallpaper == '':
      self.current_wallpaper = _("change this with picture file")

    # workspace node list
    # fill with workspace node if the type is workspace
    if self.wallpapoz_type == "workspace":
      self.workspace_node_list = self.wallpapoz_node.getElementsByTagName("workspace")
    # fill with file node if the type is desktop
    else:
      self.workspace_node_list = self.wallpapoz_node.getElementsByTagName("file")

  # reparse wallpapoz xml configuration file
  def reparse_xml(self):
    # okay, parse the xml file
    try:
      self.xmldoc = minidom.parse(self.config_file)
    except xml.parsers.expat.ExpatError:
      print _("The configuration file is corrupted. Remove it then create a new one again with Wallpapoz!")
      sys.exit()

    # wallpapoz node
    self.wallpapoz_node = self.xmldoc.childNodes[1]

    # wallpapoz type ( workspace or desktop )
    self.wallpapoz_type = self.wallpapoz_node.attributes["type"].value

    # workspace node list
    # fill with workspace node if the type is workspace
    if self.wallpapoz_type == "workspace":
      self.workspace_node_list = self.wallpapoz_node.getElementsByTagName("workspace")
    # fill with file node if the type is desktop
    else:
      self.workspace_node_list = self.wallpapoz_node.getElementsByTagName("file")

  ## class method -- get delay time that wallpaper list thread manipulate its index
  def delay(self):
    return self.wallpapoz_node.attributes["interval"].value

  ## class method -- whether the wallpaper list thread randomize its index
  def is_random(self):
    return self.wallpapoz_node.attributes["random"].value

  ## class method -- set delay time
  def set_delay(self, time):
    self.wallpapoz_node.setAttribute('interval', time)

  # set style attribute (fill screen, center, zoom, etc)
  def set_style(self, style):
    self.wallpapoz_node.setAttribute('style', style)

  # get style attribute (fill screen, center, zoom, etc)
  def style(self):
    try:
      return self.wallpapoz_node.attributes["style"].value
    except KeyError:
      # default is centered
      return "2"

  # get type attribute (desktop or workspace)
  def get_type(self):
    try:
      return self.wallpapoz_node.attributes["type"].value
    except KeyError:
      return "workspace"

  # get changing wallpaper when changing workspace
  def change_wallpaper_when_changing_workspace(self):
    try:
      if self.wallpapoz_node.attributes["type"].value == 'desktop':
        return False
      elif self.wallpapoz_node.attributes["type"].value == 'workspace':
        return True
    except KeyError:
      return True

  # get type of window manager
  def get_window_manager(self):
    return self.wallpapoz_window_manager

  ## class method -- set random
  def set_random(self, randm):
    if randm:
      self.wallpapoz_node.setAttribute('random', "1" )
    else:
      self.wallpapoz_node.setAttribute('random', "0" )

  # fill list with wallpaper path file from xml file
  def fill_list(self):
    # container for wallpapers list
    worklist = []

    # if our configuration file is for workspace
    # I mean when user change workspace, the wallpaper change
    if self.wallpapoz_type == "workspace":

      # for every workspace we have in current desktop
      # so if we have 4 workspace, worklist will be like this:
      # [ [], [], [], [] ]
      for i in range(self.workspace_num):
        worklist.append( [] )

      # workspace number
      index = -1

      # remember this is our xml file
      # <workspace name="blabla">
      #   <file>bla.jpg</file>
      #   <file>buu.jpg</file>
      #   .....
      # </workspace>
      # <workspace name="gaga">
      #   <file>....

      # workspace_node hold <workspace name="blabla">
      for workspace_node in self.workspace_node_list:
        # file_node_list hold all <file> below <workspace...>
        file_node_list = workspace_node.getElementsByTagName('file')

        # our treeview example
        # workspace             wallpaper
        # >1                    nature
        #  >1                    sunset.jpg
        #  >2                    moon.png
        # >2                    sexy girls
        #  >1                    britney.jpg

        # the corresponding xml file will be like this:
        # <workspace name="nature">
        #   <file>sunset.jpg</file>
        #   <file>moon.png</file>
        # </workspace>
        # <workspace name="sexy girls">
        #   <file>britney.jpg</file>

        # index hold workspace number, that is number in the left of "nature" and "sexy girls"
        index = index + 1

        # if our workspace amount in desktop is lesser than workspace node in xml file
        # then no need to fill it again from xml file
        if len(worklist) <= index:
          break;

        # we put "name" attribute value to the first of every list inside worklist
        # <workspace name="stupid">, "name" attribute value will be "stupid"
        # so worklist will be like this in first iteration:
        # [ ["nature"], [], [], [] ]
        # example taken from above line "index = index + 1"
        worklist[index].append( workspace_node.attributes["name"].value )

        # node will hold single <file> below <workspace...>
        # we iterating all <file> below <workspace...>
        for node in file_node_list:
          # here we just interested in "file" not empty space
          # remember, this is our xml file
          # <workspace name="stupid">
          #   <file>bla.jpg</file>
          #   <file>buu.jpg</file>
          # .....
          # for first iteration, our node hold this value: emptyspace<file>bla.jpg</file>emptyspace
          # emptyspace is space between workspace node and file node
          # of course, if our xml file is like this:
          # <workspace name="stupid"><file>bla.jpg</file><file>buu.jpg</file>....
          # there is no emptyspace
          # but I don't like that xml file style
          if node.nodeName == "file":
            # put it in our worklist list
            worklist[index].append(node.firstChild.data)
          
          # remember our xml file, upthere
          # after iterating all of it, our worklist will be like this:
          # [ ["nature", "sunset.jpg", "moon.png"], [], [], [] ]
          # so worklist is designed to hold data like this:
          # [ [name_of_wallpapers_group1, wallpaper1, wallpaper2,...], [name_of_wallpapers_group2, wallpaper1,....],...]
          # remember, the first data of every list inside worklist list is name of wallpaper group like "nature",
          # "sexy girls". The second data and so on will hold wallpapers data
      
      # if our workspace in desktop is larger than workspace node amount in xml file
      # we must add the rest with "rename this" on wallpapers group name
      # and for every workspace of the rest give one wallpaper, that is current wallpaper
      # for example:
      # our workspace in desktop is 10
      # our workspace node in xml file is 8 ( maybe after creating the configuration file
      #                                       for the first time, we add the workspace )
      # our worklist is like this for the first time
      # [ ["nature", ...],...,["8th workspace",...], [], [] ]
      # after our worklist going through this iteration, it will be like this:
      # [ ["nature", ...],...,["8th workspace",...], ["rename this", current_wallpaper], ["rename this", current_wallpaper] ]
      index = index + 1
      if index < self.workspace_num:
        for i in range(self.workspace_num - index):
          worklist[index].append(_("rename this"))
          worklist[index].append(self.current_wallpaper)
          index += 1

    # if our configuration file is for desktop,
    # we don't change wallpaper when user change workspace
    else:
      # file_node hold <file>blabla.jpg</file>
      for file_node in self.workspace_node_list:
        # put it in our worklist list
        worklist.append(file_node.firstChild.data)

    return worklist

  # save the xml file
  def save(self):
    xml_file = open(self.config_file, "w")
    xml_file.write( self.xmldoc.toxml("utf-8") )

  # fill list with default value
  def default_fill_list(self, type):
    default_list = []
    if type == "treestore":
      for i in range(self.workspace_num):
        default_list.append([])
        default_list[i].append(_("rename this"))
        default_list[i].append(self.current_wallpaper)
    elif type == "liststore":
      default_list.append(self.current_wallpaper)
    return default_list

  ## class method -- create configuration file
  def create_configuration_file(self, wallpaperlist, tree_type):

    # use minidom implementation
    impl = minidom.getDOMImplementation()

    # this is the documenttype and document
    doctype = impl.createDocumentType("Wallpapoz", None, None)
    newdoc = impl.createDocument(None, "wallpapoz", doctype)

    # root element ( wallpapoz )
    top_element = newdoc.documentElement

    # pretty printing
    space_wallpapoz = newdoc.createTextNode("\n")
    top_element.appendChild(space_wallpapoz)
    # end of pretty printing

    # put attributes to wallpapoz element
    if self.xmldoc:
      top_element.setAttribute('random', self.is_random())
      top_element.setAttribute('interval', self.delay())
      top_element.setAttribute('style', self.style())
    else:
      top_element.setAttribute('random', '0')
      top_element.setAttribute('interval', '5')
      top_element.setAttribute('style', '2')

    # put type attributes to wallpapoz element and make the xml file
    if tree_type == "liststore":
      top_element.setAttribute('type', "desktop")

      # create file node based on wallpaper list
      for filepath in wallpaperlist:
        fileelement = newdoc.createElement("file")

        # pretty printing
        space_workspace_tab = newdoc.createTextNode("    ")
        top_element.appendChild(space_workspace_tab)
        # end of pretty printing

        # put wallpaper path to file node text
        wallpaper_path = newdoc.createTextNode(filepath)
        fileelement.appendChild(wallpaper_path)

        # add file node to top element
        top_element.appendChild(fileelement)

        # pretty printing
        space_file = newdoc.createTextNode("\n")
        top_element.appendChild(space_file)
        # end of pretty printing

    elif tree_type == "treestore":
      top_element.setAttribute('type', "workspace")

      index_of_wallpaperlist = 1

      # create workspace node based on wallpaper list
      for workspace in wallpaperlist:
        workspaceelement = newdoc.createElement("workspace")
        workspaceelement.setAttribute("no", str(index_of_wallpaperlist) )
        workspaceelement.setAttribute("name", workspace.pop(0) )

        # add the index
        index_of_wallpaperlist += 1

        # pretty printing
        space_workspace_tab = newdoc.createTextNode("    ")
        top_element.appendChild(space_workspace_tab)
        space_workspace = newdoc.createTextNode("\n")
        workspaceelement.appendChild(space_workspace)
        # end of pretty printing

        for file in workspace:

          # pretty printing
          space_file_tab = newdoc.createTextNode("        ")
          workspaceelement.appendChild(space_file_tab)
          # end of pretty printing

          fileelement = newdoc.createElement("file")
          path = newdoc.createTextNode(file)
          fileelement.appendChild(path)
          workspaceelement.appendChild(fileelement)

          # pretty printing
          space_file = newdoc.createTextNode("\n")
          workspaceelement.appendChild(space_file)
          # end of pretty printing 

        # pretty printing
        space_file_tab = newdoc.createTextNode("    ")
        workspaceelement.appendChild(space_file_tab)
        # end of pretty printing

        top_element.appendChild(workspaceelement)

        # pretty printing
        space = newdoc.createTextNode("\n")
        top_element.appendChild(space)
        # end of pretty printing

    # create it
    xml_file = open(self.config_file, "w")
    xml_file.write( newdoc.toxml("utf-8") )
