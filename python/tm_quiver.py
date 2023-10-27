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
from tmpy.capture import CaptureStdout

# Reference https://www.python.org/dev/peps/pep-0616/
def removeprefix(self, prefix):
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]

def removesuffix(self, suffix):
    # suffix='' should not call self[:-0].
    if suffix and self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]


class Quiver(LaTeX):
    def __init__(self, name = "quiver"):
        super(Quiver, self).__init__()
        self.name = name
        the_plugin_path = get_plugin_path(name)

        self.pre_code = """
\\documentclass[tikz]{standalone}
\\usepackage{amsmath}
\\input "%s/latex/quiver.sty"
\\begin{document}
""" % (the_plugin_path)
        self.post_code = """
\\end{document}
"""
        self.message = "TeXmacs interface to quiver 1.1.0"

    def available(self):
        if not super(Quiver, self).available():
            return False
        for sty in ("standalone", "tikz"):
            if len (super(Quiver, self).kpsewhich(sty + ".sty")) <= 0:
                flush_err ("Failed to find " + sty +".sty,"
                           " please install the missing LaTeX packages\n")
                return False
        return True

    def strip_comments(self, code):
        result = ''
        for line in code.split("\n"):
            if not line.startswith('%'):
                result = result + line + '\n'
        return result
        
    def evaluate(self, code):
        code = self.strip_comments(code)
        code = code.lstrip(' ').rstrip(' ')
        code = code.lstrip('\n').rstrip('\n')
        code = removeprefix(code, "\\[")
        code = removesuffix(code, "\\]")
        code = self.pre_code + "\n" + code + "\n" + self.post_code
        super(Quiver, self).evaluate(code)

    # For Debugging
    # def after_evaluate(self):
    #    self.remove_tmp_dir()


if (exists (tmpy_home_path)):
        flush_verbatim ("WARNING: You are under develop mode using " + tmpy_home_path)
        flush_newline (2)

my_globals   = {}

text = 'import builtins as __builtins__'
CaptureStdout.capture (text, my_globals, "tm_quiver")

current = Quiver()
if not current.available():
    flush_err ("Failed to launch the Quiver plugin, aborted!!!")
    exit(-1)

current.greet()
current.main_loop()

