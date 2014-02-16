#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gettext

APP = "wallpapoz"
DIR = "../share/locale"
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

_ = gettext.gettext
