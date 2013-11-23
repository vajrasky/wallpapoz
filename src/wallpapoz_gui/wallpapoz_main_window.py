from tkinter import Frame, TOP, LEFT, Y, YES, BOTH
from tkinter.ttk import Treeview

def _maketree(parent_tree, wallpapers, conf):
    tree = Treeview(parent_tree)
    i = 0
    if conf['type'] == 'workspace':
        for workspace, wallpaper_files in wallpapers.items():
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
    tree.pack()

def makemainwindow(parent, wallpapers, conf):
    main_window = Frame(parent)
    tree_window = Frame(main_window)
    image_window = Frame(main_window)

    main_window.pack(side=TOP, fill=BOTH, expand=YES)
    image_window.pack(side=TOP, fill=Y)
    tree_window.pack(side=LEFT, fill=BOTH, expand=YES)
    _maketree(tree_window, wallpapers, conf)
