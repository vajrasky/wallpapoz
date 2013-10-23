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
    menu.add_command(label=_('Help'), command=launch_help_window)
    menu.add_separator()
    menu.add_command(label=_('About'), command=menu_command_about)
    fbutton.config(menu=menu)

    return menubar
