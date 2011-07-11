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

import os, getopt, sys

VERSION = '0.1b'

TEMP_DIR = '__temp'

PAGES_ON_LIST = 4
LISTS_IN_BOOKLETE = 5

INPUT_FILE = 'input.ps'
OUTPUT_PREFIX = 'book'
PAGES = [[1, 70], [75, 75], [85, 100]]
CHAPTERS_FIRST_PAGES = [21, 40, 85]

def printUsage():
	'Print script usage information'
	print '''python booknagar.py [-h] [-v] [--help] [--version]

	-h, --help to view this help
	-v, --version to print program version number
'''

def printVersion():
	'Print script version'
	print VERSION

def constructCommand(command, arguments):
	return command + ' ' + arguments + ';'

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

# Script preparation
# ==================

try:
	os.mkdir(TEMP_DIR)
except:
	temp_dir_created = False
else:
	temp_dir_created = True

PAGES.sort()
CHAPTERS_FIRST_PAGES.sort()

if CHAPTERS_FIRST_PAGES[0] != PAGES[0][0]:
	CHAPTERS_FIRST_PAGES.insert(0, PAGES[0][0])

COMMAND_STRING = constructCommand('mkdir', OUTPUT_PREFIX)

# Select chapters ranges
# ======================

# TODO: need refactoring !!!
#       I can't believe, that I wrote this code. *facepalm*
for chapter_first_page in CHAPTERS_FIRST_PAGES:
	for page_range in PAGES:
		if chapter_first_page in range(page_range[0], page_range[1]):
			range_index = PAGES.index(page_range)
			if page_range[0] != chapter_first_page:
				PAGES.insert(range_index+1, [page_range[0], chapter_first_page-1])
				PAGES.insert(range_index+2, [chapter_first_page, page_range[1]])
				PAGES.remove(page_range)

new_pages = []
for chapter_index in range(len(CHAPTERS_FIRST_PAGES)):
	chapter_ranges = []
	for page_range in PAGES:
		curr_chap_starts = CHAPTERS_FIRST_PAGES[chapter_index]
		try:
			next_chap_starts = CHAPTERS_FIRST_PAGES[chapter_index+1]
		except IndexError:
			next_chap_starts = PAGES[len(PAGES)-1][1]
		if page_range[0] in range(curr_chap_starts, next_chap_starts-1):
			chapter_ranges.append(page_range)
	new_pages.append(chapter_ranges)
PAGES = new_pages

# TODO: debug
print PAGES

sys.exit(3)
# debug ends

# Cleaning
# ========

if temp_dir_created:
	os.rmdir(TEMP_DIR)

# ----------------------------------------------------------------------------

chapNumber = 19
pagesNumber = 14

currentBookleteNumber = 1

while (currentBookleteNumber-1) *  LISTS_IN_BOOKLETE < pagesNumber :
	execStr = "psselect -p "

	maxPage = LISTS_IN_BOOKLETE  # currentBookleteNumber
	if maxPage > pagesNumber :
		maxPage = pagesNumber

	minPage = (currentBookleteNumber-1)  # LISTS_IN_BOOKLETE + 1

	chapStr = str(chapNumber) + "_" + str(currentBookleteNumber)

	execStr += str(minPage) + "-" + str(maxPage) + " chap" + str(chapNumber) + ".ps "
	execStr += "chap" + chapStr + ".ps; psbook chap" + chapStr + ".ps | psnup -2 -l -p a4 > print"
	execStr += chapStr + ".ps; rm chap" + chapStr + ".ps"
	print execStr

	currentBookleteNumber += 1

print "mkdir " + str(chapNumber) + "; rm -f chap" + str(chapNumber) + "*" + "; mv print" + str(chapNumber) + "_* " + str(chapNumber)
