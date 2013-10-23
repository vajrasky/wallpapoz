from tkinter import Frame, TOP, X, Y
from tkinter.ttk import Treeview

def _maketree(parent_tree, workspaces):
    tree = Treeview(parent_tree)
    i = 0
    for workspace, wallpapers in workspaces.items():
        i += 1
        index = str(i)
        tree.insert('', 'end', index, text=workspace)
        for j, wallpaper in enumerate(wallpapers):
            inner_index = index + '_' + str(j)
            tree.insert(index, 'end', inner_index, text=wallpaper)
    tree.pack()

def makemainwindow(parent, workspaces):
    main_window = Frame(parent)
    tree_window = Frame(main_window)
    image_window = Frame(main_window)
    main_window.pack(side=TOP, fill=X)
    tree_window.pack(side=TOP, fill=Y)
    _maketree(tree_window, workspaces)
    image_window.pack(side=TOP, fill=Y)
