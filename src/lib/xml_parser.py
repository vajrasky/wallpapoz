from xml.dom import minidom


def parse_wallpapoz_file(wallpapoz_setting_file):
    """
    Parses wallpapoz configuration file, expected found in ~/.wallpapoz/wallpapoz.xml.
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
        workspaces = {}
        for workspace_element in workspaces_elements:
            workspace_name = workspace_element.attributes['name'].value
            workspaces[workspace_name] = []
            for element in workspace_element.childNodes:
                if isinstance(element, minidom.Element):
                    workspaces[workspace_name].append(element.childNodes[0].data)
        return workspaces, conf

    elif wallpapoz_type == 'desktop':
        files_elements = xmldoc.getElementsByTagName('file')
        files = []
        for file_element in files_elements:
            if isinstance(file_element, minidom.Element):
                files.append(file_element.childNodes[0].data)
        return files, conf

    return None
