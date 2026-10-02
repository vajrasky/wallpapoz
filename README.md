# Wallpapoz

Wallpapoz is a Linux desktop wallpaper rotation tool. It can rotate wallpapers
on a timer, and it can keep separate wallpaper lists for different workspaces.

This branch is the modern Python 3 / GTK 4 version. The old GTK 2, Tkinter,
legacy daemon, Glade, and installer files are preserved under `old/`.

## Current Status

The GTK 4 app can:

- read and write the existing `~/.wallpapoz/wallpapoz.xml` configuration file
- manage workspace or desktop wallpaper lists
- add wallpaper files or folders
- preview selected wallpaper files
- save interval, random order, workspace mode, and style settings

The Python 3 daemon supports GNOME, MATE, Cinnamon, XFCE, Fluxbox, and KDE Plasma.
KDE uses `gdbus` to update wallpapers on all screens in the current activity.
Workspace detection supports X11 desktops and Compiz viewport grids, using the
actual screen size. On Wayland, workspace detection depends on what the session
exposes through X11 compatibility tools.

Each workspace keeps its selected image until its own interval expires. Switching
away and back restores that image, including in random mode, without resetting
the timer. An expired workspace advances when it is next visited.

## Dependencies

Install GTK 4 and PyGObject from your Linux distribution. Do not install `gi`
from pip.

Debian or Ubuntu:

```sh
sudo apt update
sudo apt install python3-gi gir1.2-gtk-4.0 python3-pil
```

Fedora:

```sh
sudo dnf install python3-gobject gtk4 python3-pillow
```

Arch Linux:

```sh
sudo pacman -S python-gobject gtk4 python-pillow
```

Optional desktop integration tools:

```sh
sudo apt install x11-utils
```

For KDE Plasma, also install `libglib2.0-bin` to provide `gdbus` on Debian/Ubuntu.
The Plasma shell must be running in the same user session.

## Development Setup

Using `uv` is recommended, with access to system site packages so the virtual
environment can see the distro-provided GTK bindings:

```sh
uv venv --system-site-packages --prompt wallpapoz
source .venv/bin/activate
```

Verify GTK:

```sh
python -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk; print(Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION)"
```

## Run

Start the GTK 4 configuration app:

```sh
python src/wallpapoz_gtk4.py
```

Check the daemon configuration without changing your wallpaper:

```sh
python src/daemon_wallpapoz_py3.py --check
```

Run the daemon:

```sh
python src/daemon_wallpapoz_py3.py
```

The daemon changes your wallpaper according to `~/.wallpapoz/wallpapoz.xml`.

## Sample Wallpapers

Sample PNG files are included under `samples/` for quick testing. Regenerate
them with:

```sh
python scripts/create_sample_wallpapers.py
```

## Local Install

For a simple per-user install from this checkout, create wrappers in
`~/.local/bin`:

```sh
mkdir -p ~/.local/bin
ln -sf "$PWD/src/wallpapoz_gtk4.py" ~/.local/bin/wallpapoz
ln -sf "$PWD/src/daemon_wallpapoz_py3.py" ~/.local/bin/daemon_wallpapoz
```

Make sure `~/.local/bin` is in your `PATH`:

```sh
echo "$PATH" | grep -q "$HOME/.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
```

Then run:

```sh
wallpapoz
daemon_wallpapoz --check
```

To use the desktop launcher, copy the desktop file and icon:

```sh
mkdir -p ~/.local/share/applications ~/.local/share/icons/hicolor/256x256/apps
cp share/wallpapoz/wallpapoz.desktop ~/.local/share/applications/
cp share/wallpapoz/images/wallpapoz.png ~/.local/share/icons/hicolor/256x256/apps/wallpapoz.png
```

Log out and back in if your desktop shell does not immediately pick up the new
launcher.

## Tests

Run:

```sh
python3 -m unittest discover -s src/tests
python3 -m py_compile src/wallpapoz_gtk4.py src/daemon_wallpapoz_py3.py src/lib/wallpaper_system.py src/lib/xml_parser.py
```

## Legacy Code

The old project files are kept in `old/` for reference:

- `old/src/wallpapoz`
- `old/src/daemon_wallpapoz`
- `old/src/wallpapoz_tkinter.py`
- `old/src/wallpapoz_gui/`
- `old/share/wallpapoz/glade/`
- `old/share/wallpapoz/lib/`
- `old/setup.py`
- `old/README`
