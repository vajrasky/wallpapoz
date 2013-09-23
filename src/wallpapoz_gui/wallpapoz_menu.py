# -*- coding: utf-8 -*-

#=============================================================================
#
#   wallpapoz_menu.py - Wallpapoz
#   Copyright (C) 2013 Vajrasky Kok <sky.kok@speaklikeaking.com>
#
#=============================================================================
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#=============================================================================

## The gui menu

from tkinter import *
from tkinter.messagebox import *

from lib.gettext import _

from wallpapoz_gui.wallpapoz_menu_commands import *

def notdone():
    showerror('Not implemented', 'Not yet available')

def makemenu(parent):
    menubar = Frame(parent)
    menubar.pack(side=TOP, fill=X)

    fbutton = Menubutton(menubar, text=_('File'), underline=0)
    fbutton.pack(side=LEFT)
    menu = Menu(fbutton, tearoff=False)
    menu.add_command(label=_('Add Wallpapers (File)'), command=notdone)
    menu.add_command(label=_('Add Wallpapers (Directory)'), command=notdone)
    menu.add_command(label=_('Save'), command=notdone)
    menu.add_separator()
    menu.add_command(label=_('Quit'), command=notdone)
    fbutton.config(menu=menu)

    fbutton = Menubutton(menubar, text=_('Edit'), underline=0)
    fbutton.pack(side=LEFT)
    menu = Menu(fbutton, tearoff=False)
    menu.add_command(label=_('Cut'), command=notdone)
    menu.add_command(label=_('Copy'), command=notdone)
    menu.add_command(label=_('Paste'), command=notdone)
    menu.add_separator()
    menu.add_command(label=_('Rename Workspace'), command=notdone)
    menu.add_command(label=_('Change Wallpaper'), command=notdone)
    menu.add_command(label=_('Delete Wallpapers'), command=notdone)
    menu.add_command(label=_('Move Up'), command=notdone)
    menu.add_command(label=_('Move Down'), command=notdone)
    menu.add_separator()
    menu.add_command(label=_('Preferences'), command=notdone)
    fbutton.config(menu=menu)

    fbutton = Menubutton(menubar, text=_('Daemon'), underline=0)
    fbutton.pack(side=LEFT)
    menu = Menu(fbutton, tearoff=False)
    menu.add_command(label=_('Start'), command=notdone)
    menu.add_command(label=_('Restart'), command=notdone)
    menu.add_command(label=_('Stop'), command=notdone)
    fbutton.config(menu=menu)

    fbutton = Menubutton(menubar, text=_('Help'), underline=0)
    fbutton.pack(side=LEFT)
    menu = Menu(fbutton, tearoff=False)
    menu.add_command(label=_('Help'), command=notdone)
    menu.add_separator()
    menu.add_command(label=_('About'), command=menu_command_about)
    fbutton.config(menu=menu)

    return menubar
