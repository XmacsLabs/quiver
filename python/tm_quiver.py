#!/usr/bin/env python3
###############################################################################
##
## MODULE      : tm_quiver.py
## DESCRIPTION : Launcher for the quiver plugin
## COPYRIGHT   : (C) 2021  Da Shen
##
## This software falls under the GNU general public license version 3 or later.
## It comes WITHOUT ANY WARRANTY WHATSOEVER. For details, see the file LICENSE
## in the root directory or <http://www.gnu.org/licenses/gpl-3.0.html>.

import os
import sys
from os.path import exists

tmpy_home_path = os.environ.get("TEXMACS_HOME_PATH") + "/plugins/tmpy"
if (exists (tmpy_home_path)):
    sys.path.append(os.environ.get("TEXMACS_HOME_PATH") + "/plugins/")
else:
    sys.path.append(os.environ.get("TEXMACS_PATH") + "/plugins/")

from subprocess import Popen, PIPE, STDOUT
from tmpy.graph.latex import LaTeX
from tmpy.protocol import *


class Quiver(LaTeX):
    def __init__(self, name = "quiver"):
        super(Quiver, self).__init__()
        self.name = name
        the_plugin_path = get_plugin_path(name)

        self.pre_code = """
\\usepackage{quiver}
\\input "%s/latex/quiver.sty"
\\begin{document}
""" % (the_plugin_path)
        self.post_code = """
\\end{document}
"""
        self.message = "TeXmacs interface to quiver 1.1.0"

    def available(self):
        if not super(LaTeX, self).available():
            return False
        for sty in ("standalone", "tikz"):
            if len (super(TikZ, self).kpsewhich(sty + ".sty")) <= 0:
                flush_err ("Failed to find " + sty +".sty,"
                           " please install the missing LaTeX packages\n")
                return False
        return True
        
    def evaluate(self, code):
        code = self.pre_code + "\n" + code + "\n" + self.post_code
        super(Quiver, self).evaluate(code)

