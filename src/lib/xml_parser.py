from xml.dom import minidom
from xml.etree import ElementTree


def parse_wallpapoz_file(wallpapoz_setting_file):
    """
    Parses wallpapoz configuration file, expected found in
    ~/.wallpapoz/wallpapoz.xml.

    Returns dictionary of workspaces including the wallpaper paths or list of
    wallpaper paths or None if the configuration file is corrupted.
    """
    xmldoc = minidom.parse(wallpapoz_setting_file)
    wallpapoz_element = xmldoc.lastChild
    conf = {}

    for item in wallpapoz_element.attributes.items():
        conf[item[0]] = item[1]
    wallpapoz_type = wallpapoz_element.attributes['type'].value

    if wallpapoz_type == 'workspace':
        workspaces_elements = xmldoc.getElementsByTagName('workspace')
        workspaces = []

        for workspace_element in workspaces_elements:
            workspace_name = workspace_element.attributes['name'].value
            workspaces.append((workspace_name, []))

            for element in workspace_element.childNodes:
                if isinstance(element, minidom.Element):
                    workspaces[-1][1].append(element.childNodes[0].data)
        return workspaces, conf

    elif wallpapoz_type == 'desktop':
        files_elements = xmldoc.getElementsByTagName('file')
        files = []

        for file_element in files_elements:
            if isinstance(file_element, minidom.Element):
                files.append(file_element.childNodes[0].data)
        return files, conf

    return None

def save_treeview_to_wallpapoz_file(f, type, elements, *, interval, random, style):
    root = ElementTree.Element("wallpapoz")
    root.set("interval", interval)
    root.set("random", random)
    root.set("style", style)
    root.set("type", type)
    if type=="workspace":
        id = 1
        for key, files in elements.items():
            workspace_elem = ElementTree.SubElement(root, "workspace")
            workspace_elem.set("name", key)
            workspace_elem.set("id", str(id))
            id += 1
            for file in files:
                file_elem = ElementTree.SubElement(workspace_elem, "file")
                file_elem.text = file
    elif type=="desktop":
        for file in elements:
            file_elem = ElementTree.SubElement(root, "file")
            file_elem.text = file
    tree = ElementTree.ElementTree(root)
    tree.write(f, "utf-8", True)
