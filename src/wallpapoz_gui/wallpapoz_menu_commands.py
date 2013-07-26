# -*- coding: utf-8 -*-

#=============================================================================
#
#   wallpapoz_menu_commands.py - Wallpapoz
#   Copyright (C) 2013 Sky Kok <sky.kok@speaklikeaking.com>
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

## The gui menu commands

from tkinter import *

from lib.gettext import _

import os.path
from PIL import ImageTk, Image

def menu_command_about():
    about_win = Toplevel()

    wallpapoz_logo_path = os.path.dirname(os.path.abspath(__file__)) +\
        '/../../share/wallpapoz/images/wallpapoz.png'
    if os.path.exists(wallpapoz_logo_path):
        img = Image.open(wallpapoz_logo_path)
        logo = ImageTk.PhotoImage(img)
        image_label = Label(about_win, image=logo)
        image_label.pack()
        image_label.image = logo

    wallpapoz_label = Label(about_win,
                            text='wallpapoz',
                            font=('courier', 20, 'bold'))
    wallpapoz_label.pack()

    unix_label = Label(about_win,
                       text=_('Unix Desktop Wallpapers '
                              'Configuration System'),
                       font=('courier', 12))
    unix_label.pack()

    copyright_label = Label(about_win, text=_('Copyright') +
                                            ' @ 2004 - 2013 Vajrasky Kok')
    copyright_label.pack()

    def click_wallpapoz_website_label(event):
        import webbrowser
        webbrowser.open('http://vajrasky.wordpress.com/wallpapoz')

    wallpapoz_website_label = Label(about_win,
                                    text=_('Wallpapoz Website'),
                                    font=('courier', 11, 'underline'),
                                    fg='blue')
    wallpapoz_website_label.bind('<Button-1>', click_wallpapoz_website_label)
    wallpapoz_website_label.pack()

    buttons_frame = Frame(about_win)
    Button(buttons_frame, text='Credits', command=about_win.destroy)\
        .pack(side=LEFT)
    Button(buttons_frame, text='License', command=about_win.destroy)\
        .pack(side=LEFT)
    Button(buttons_frame, text='Close', command=about_win.destroy)\
        .pack(side=LEFT)
    buttons_frame.pack()

    about_win.title(_('about wallpapoz'))
    about_win.focus_set()
    about_win.grab_set()
