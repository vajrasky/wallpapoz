import json
import os
import re
import subprocess
from pathlib import Path


STYLE_BY_DESKTOP = {
    "kde": {"3": 2, "2": 1, "1": 0, "0": 6, "4": 3},
    "gnome": {"3": "zoom", "2": "scaled", "1": "stretched", "0": "centered", "4": "wallpaper"},
    "mate": {"3": "zoom", "2": "scaled", "1": "stretched", "0": "centered", "4": "wallpaper"},
    "cinnamon": {"3": "zoom", "2": "scaled", "1": "stretched", "0": "centered", "4": "wallpaper"},
    "xfce": {"3": "5", "2": "4", "1": "3", "0": "1", "4": "2"},
    "fluxbox": {"3": "--bg-fill", "2": "--bg-max", "1": "--bg-fill", "0": "--bg-center", "4": "--bg-tile"},
}


class WallpaperSystem:
    def __init__(self):
        self.desktop = self._detect_desktop()

    def _detect_desktop(self):
        current = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        session = os.environ.get("DESKTOP_SESSION", "").lower()
        combined = f"{current} {session}"

        if "kde" in combined or "plasma" in combined:
            return "kde"
        if "xfce" in combined:
            return "xfce"
        if "mate" in combined:
            return "mate"
        if "cinnamon" in combined:
            return "cinnamon"
        if "fluxbox" in combined:
            return "fluxbox"
        return "gnome"

    def _workspace_state(self):
        properties = (
            "_NET_NUMBER_OF_DESKTOPS", "_NET_CURRENT_DESKTOP",
            "_NET_DESKTOP_GEOMETRY", "_NET_DESKTOP_VIEWPORT",
        )
        output = self._run_output(["xprop", "-root", *properties])
        values = {}
        for line in output.splitlines():
            match = re.fullmatch(
                r"(_NET_\w+)\([^)]*\)\s*=\s*(\d+(?:\s*,\s*\d+)*)\s*", line
            )
            if match:
                values[match.group(1)] = [int(v) for v in match.group(2).split(",")]
        count = max(values.get(properties[0], [1])[0], 1)
        current = values.get(properties[1], [0])[0]
        geometry = values.get(properties[2], [])
        viewports = values.get(properties[3], [])
        if len(geometry) != 2 or len(viewports) < 2 * (current + 1):
            return count, current

        # Compiz represents its workspace grid as viewports on a large desktop.
        # Use the whole X screen, including all monitors, as the viewport size.
        dimensions = self._run_output(["xwininfo", "-root"])
        width = re.search(r"Width:\s*(\d+)", dimensions)
        height = re.search(r"Height:\s*(\d+)", dimensions)
        if not width or not height:
            return count, current
        width, height = int(width.group(1)), int(height.group(1))
        if not width or not height:
            return count, current
        if geometry[0] % width or geometry[1] % height:
            return count, current
        columns, rows = geometry[0] // width, geometry[1] // height
        if columns < 1 or rows < 1:
            return count, current
        x, y = viewports[2 * current:2 * current + 2]
        if not (0 <= x < geometry[0] and 0 <= y < geometry[1]):
            return count, current
        cells = columns * rows
        return count * cells, current * cells + (y // height) * columns + x // width

    def total_workspaces(self):
        return self._workspace_state()[0]

    def current_workspace(self):
        return self._workspace_state()[1]

    def set_wallpaper(self, filename, style_key):
        filename = str(Path(filename).expanduser())
        style = STYLE_BY_DESKTOP.get(self.desktop, STYLE_BY_DESKTOP["gnome"]).get(style_key, "scaled")

        if self.desktop == "kde":
            # Serialize data before embedding it in Plasma's JavaScript API.
            uri = json.dumps(Path(filename).absolute().as_uri())
            fill_mode = STYLE_BY_DESKTOP["kde"].get(style_key, 1)
            script = f"""
                var allDesktops = desktopsForActivity(currentActivity());
                for (var i = 0; i < allDesktops.length; i++) {{
                    var d = allDesktops[i];
                    d.wallpaperPlugin = "org.kde.image";
                    d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
                    d.writeConfig("Image", {uri});
                    d.writeConfig("FillMode", {fill_mode});
                }}
            """
            subprocess.run([
                "gdbus", "call", "--session", "--dest", "org.kde.plasmashell",
                "--object-path", "/PlasmaShell", "--method",
                "org.kde.PlasmaShell.evaluateScript", script,
            ], check=True, stdout=subprocess.DEVNULL)
        elif self.desktop == "gnome":
            uri = Path(filename).absolute().as_uri()
            self._run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri])
            self._run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri])
            self._run(["gsettings", "set", "org.gnome.desktop.background", "picture-options", style])
        elif self.desktop == "mate":
            self._run(["gsettings", "set", "org.mate.background", "picture-filename", filename])
            self._run(["gsettings", "set", "org.mate.background", "picture-options", style])
        elif self.desktop == "cinnamon":
            uri = Path(filename).absolute().as_uri()
            self._run(["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", uri])
            self._run(["gsettings", "set", "org.cinnamon.desktop.background", "picture-options", style])
        elif self.desktop == "xfce":
            self._run(
                [
                    "xfconf-query",
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor0/image-path",
                    "-s",
                    filename,
                ]
            )
            self._run(
                [
                    "xfconf-query",
                    "-c",
                    "xfce4-desktop",
                    "-p",
                    "/backdrop/screen0/monitor0/image-style",
                    "-s",
                    style,
                ]
            )
        elif self.desktop == "fluxbox":
            self._run(["feh", style, filename])

    def _run(self, command):
        try:
            subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            return

    def _run_output(self, command):
        try:
            result = subprocess.run(command, check=False, text=True, capture_output=True)
        except FileNotFoundError:
            return ""
        return result.stdout
