#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=============================================================================
#
#    Installation
#    Copyright (C) 2012 Vajrasky Akbar Kok <arjuna@vajrasky.net>
#
#=============================================================================
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#=============================================================================

import os
import sys
import getopt
import shutil
import gettext

# so we can call from anywhere
pathname = os.path.dirname(sys.argv[0])
os.chdir(os.path.abspath(pathname))

# i18n
APP = "wallpapoz"
DIR = "share/locale"
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext

usage_info = _("""
This script installs or uninstalls Wallpapoz on your system.
If you encounter any bugs, please report them to arjuna@vajrasky.net.

-------------------------------------------------------------------------------

Usage:

 ./setup.py install              ---      Install to /usr/local

 ./setup.py uninstall            ---      Uninstall from /usr/local

-------------------------------------------------------------------------------

Options:

 --installdir <directory>          ---      Install or uninstall in <directory>
                                            instead of /usr/local
""")


def info():
    print usage_info
    sys.exit(1)


def install(src, dst=None):
    if not dst:
        dst = src

    try:
        dst = os.path.join(install_dir, dst)
        assert os.path.isfile(src)
        assert not os.path.isdir(dst)

        if not os.path.isdir(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        shutil.copy2(src, dst)

        print _("Installed"), dst
    except:
        print _("Error while installing"), dst


def uninstall(path):
    try:
        path = os.path.join(install_dir, path)

        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            return

        print _("Removed"), path
    except:
        print _("Error while removing"), path


def check_libs():
    req_deps = ['pygtk', 'gtk.glade', 'PIL']

    for dep in req_deps:
        try:
            __import__(dep)

            print _("Checking for %s\t\t\t\t\tOK" % dep)
        except ImportError:
            raise Exception(_("missing required dependency: %s" % dep))
        except:
            raise


def check_gnome():
    try:
        import gnome
        assert gnome._gnome.__version__ > 1
    except ImportError:
        print
        print _("Gnome Python is not found. Wallpapoz still could be used ",
                "and it has been installed.")
        print _("But it means you can not access help documentation in your ",
                "native language if it is available.")
        print
    except AssertionError:
        print
        print _("Please upgrade your gnome to at least version 2")


def check_dependencies():
    if not os.environ.get('DISPLAY'):
        import warnings
        warnings.simplefilter("ignore", Warning)

    if os.popen('which xwininfo').read():
        print _("Checking for xwininfo\t\t\t\t\tOK")
    else:
        raise Exception(_("missing xwininfo"))

    check_libs()
    check_gnome()


install_dir = "/usr/local/"
APP_ISO_CODES = ("id", "ja", "de", "sv", "es", "fr", "ru", "it", "cs", "zh_CN",
                 "pl", "tr", "hu", "pt")
DOC_ISO_CODES = ("id", "ja", "ru", "cs")

try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], "", ["installdir="])
except getopt.GetoptError:
    info()

for opt, value in opts:
    if opt == "--installdir":
        install_dir = value

        if not os.path.isdir(install_dir):
            print _("\n*** Error:"), install_dir, _("does not exist.\n")
            info()

if args == ["install"]:
    check_dependencies()

    print _("Installing Wallpapoz in"), install_dir, "...\n"

    install("src/wallpapoz", "bin/wallpapoz")
    install("src/daemon_wallpapoz", "bin/daemon_wallpapoz")
    install("src/launcher_wallpapoz.sh", "bin/launcher_wallpapoz.sh")
    install("share/wallpapoz/lib/xml_processing.py")
    install("share/wallpapoz/lib/wallpapoz_system.py")
    install("share/wallpapoz/glade/wallpapoz.glade")
    install("share/wallpapoz/glade/wallpapoz.png")
    install("share/gnome/help/wallpapoz/C/wallpapoz.xml")
    install("share/gnome/help/wallpapoz/C/legal.xml")
    install("share/wallpapoz/wallpapoz.desktop",
            "share/applications/wallpapoz.desktop")
    install("share/wallpapoz/glade/wallpapoz.png",
            "share/pixmaps/wallpapoz.png")

    for lang in APP_ISO_CODES:
        install("share/locale/" + lang + "/LC_MESSAGES/wallpapoz.mo")

    for lang in DOC_ISO_CODES:
        install("share/gnome/help/wallpapoz/" + lang + "/wallpapoz.xml")
        install("share/gnome/help/wallpapoz/" + lang + "/legal.xml")

elif args == ["uninstall"]:
    print _("Uninstalling Wallpapoz from"), install_dir, "...\n"
    uninstall("bin/wallpapoz")
    uninstall("bin/daemon_wallpapoz")
    uninstall("bin/launcher_wallpapoz.sh")
    uninstall("share/wallpapoz/lib/xml_processing.py")
    uninstall("share/wallpapoz/lib/wallpapoz_system.py")
    uninstall("share/wallpapoz/glade/wallpapoz.glade")
    uninstall("share/wallpapoz/glade/wallpapoz.png")
    uninstall("share/gnome/help/wallpapoz/C/wallpapoz.xml")
    uninstall("share/gnome/help/wallpapoz/C/legal.xml")
    uninstall("share/applications/wallpapoz.desktop")
    uninstall("share/pixmaps/wallpapoz.png")

    for lang in APP_ISO_CODES:
        uninstall("share/locale/" + lang + "/LC_MESSAGES/wallpapoz.mo")
    for lang in DOC_ISO_CODES:
        uninstall("share/gnome/help/wallpapoz/" + lang + "/wallpapoz.xml")
        uninstall("share/gnome/help/wallpapoz/" + lang + "/legal.xml")

    print
    print _("""
There might still be files in ~/.wallpapoz/ left on your system.
Please remove that directory manually if you do not plan to
install Wallpapoz again later.
""")

else:
    info()
