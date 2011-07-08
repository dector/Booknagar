# Copyright (c) 2011, dector (dector9@gmail.com) All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   - Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
#   - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
#  - Neither the name of the nor the names of its
# contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import getopt, sys

VERSION = '0.1b'

PAGES_ON_LIST = 4
PAGES_IN_BOOKLETE = 5

def printUsage():
    print '''python booknagar.py [-h] [-v] [--help] [--version]
'''

def printVersion():
    print VERSION

# Parsing arguments
# =================

# Arguments:
# -h, --help        --> for help
# -v, --version     --> for version output

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hv', ['help', 'version'])
except getopts.GetoptsError, err:
    printUsage()
    sys.exit(2)
else:
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printUsage()
            sys.exit()
        elif opt in ('-v', '--version'):
            printVersion()
            sys.exit()


# +------------------------------------+
# |                                    |
# | THIS SCRIPT IS UNDER BUILDING !!!  |
# |                 ( )                |
# |       __ __    / /|                |
# |      _==_==___/|/_/                |
# |      \_____|   |  |                |
# |        (_)     |  |                |
# +------------------------------------+

# Chapters selecting
# ==================

# Chapters preparing
# ==================

# Spliting chapters on bookletes
# ==============================

# Setting booklets on pages
# =========================

# Print
# =====
# ----------------------------------------------------------------------------

chapNumber = 19
pagesNumber = 14

currentBookleteNumber = 1

while (currentBookleteNumber-1) *  PAGES_IN_BOOKLETE < pagesNumber :
    execStr = "psselect -p "

    maxPage = PAGES_IN_BOOKLETE  # currentBookleteNumber
    if maxPage > pagesNumber :
        maxPage = pagesNumber

    minPage = (currentBookleteNumber-1)  # PAGES_IN_BOOKLETE + 1

    chapStr = str(chapNumber) + "_" + str(currentBookleteNumber)

    execStr += str(minPage) + "-" + str(maxPage) + " chap" + str(chapNumber) + ".ps "
    execStr += "chap" + chapStr + ".ps; psbook chap" + chapStr + ".ps | psnup -2 -l -p a4 > print"
    execStr += chapStr + ".ps; rm chap" + chapStr + ".ps"
    print execStr

    currentBookleteNumber += 1

print "mkdir " + str(chapNumber) + "; rm -f chap" + str(chapNumber) + "*" + "; mv print" + str(chapNumber) + "_* " + str(chapNumber)
