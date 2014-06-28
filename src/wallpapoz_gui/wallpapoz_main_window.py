from tkinter import (Frame, TOP, LEFT, Y, YES, BOTH, NO, CENTER, X, END,
                     Label, Text, BOTTOM, Checkbutton)
from tkinter.ttk import Treeview

from lib.gettext import _

tree = None

def _maketree(parent_tree, wallpapers, conf):
    global tree
    tree = Treeview(parent_tree)
    i = 0
    if conf['type'] == 'workspace':
        for workspace, wallpaper_files in wallpapers:
            i += 1
            index = str(i)
            tree.insert('', 'end', index, text=workspace)
            for j, wallpaper_file in enumerate(wallpaper_files):
                inner_index = index + '_' + str(j)
                tree.insert(index, 'end', inner_index, text=wallpaper_file)
    elif conf['type'] == 'desktop':
        for wallpaper_file in wallpapers:
            i += 1
            index = str(i)
            tree.insert('', 'end', index, text=wallpaper_file)
    tree.pack(side=TOP, expand=YES, fill=BOTH)

def _makesetting(setting_window, conf):
    setting_label = Label(setting_window,
                          text=_('Setting'),
                          font=('courier', 20, 'bold'))
    setting_label.pack()
    random_container = Frame(setting_window)
    random_container.pack(side=BOTTOM)
    random_label = Label(random_container,
                         text=_('Choose wallpaper randomly? '),
                         font=('courier', 15, 'bold'))
    random_label.pack(side=LEFT)
    random_checkbutton = Checkbutton(random_container)
    random_checkbutton.pack(side=LEFT)
    if conf['random'] == "1":
        random_checkbutton.select()
    interval_container = Frame(setting_window)
    interval_container.pack(side=BOTTOM)
    interval_label = Label(interval_container,
                           text=_('Change wallpaper every '),
                           font=('courier', 15, 'bold'))
    interval_label.pack(side=LEFT)
    interval_text = Text(interval_container, height=1, width=4)
    interval_text.insert(END, conf['interval'])
    interval_text.pack(side=LEFT)
    minute_label = Label(interval_container,
                         text=_(' minutes.'),
                         font=('courier', 15, 'bold'))
    minute_label.pack(side=LEFT)

def makemainwindow(parent, wallpapers, conf):
    main_window = Frame(parent)
    top_window = Frame(main_window)
    tree_window = Frame(top_window)
    image_window = Frame(top_window)
    bottom_window = Frame(main_window)
    setting_window = Frame(bottom_window)

    main_window.pack(side=TOP, expand=YES, fill=BOTH)
    top_window.pack(side=TOP, expand=YES, fill=BOTH)
    tree_window.pack(side=TOP, expand=YES, fill=BOTH)
    image_window.pack(side=TOP, expand=YES, fill=BOTH)
    bottom_window.pack(side=TOP, expand=YES, fill=BOTH)
    setting_window.pack(side=TOP, expand=YES, fill=BOTH)
    _maketree(tree_window, wallpapers, conf)
    _makesetting(setting_window, conf)
