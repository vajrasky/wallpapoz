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

## The main window

from tkinter import Frame, TOP, X, Y
from tkinter.ttk import Treeview

def makemainwindow(parent):
    main_window = Frame(parent)
    tree_window = Frame(main_window)
    image_window = Frame(main_window)
    main_window.pack(side=TOP, fill=X)
    tree_window.pack(side=TOP, fill=Y)
    image_window.pack(side=TOP, fill=Y)
    tree = Treeview(tree_window)
    tree.insert('', 'end', 'widgets', text='Widget Tour')
    tree.insert('widgets', 0, 'gallery', text='Applications')
    tree.pack()
