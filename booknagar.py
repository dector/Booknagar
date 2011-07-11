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

INPUT_FILE = ''
OUTPUT_PREFIX = ''
PAGES = []
CHAPTERS_FIRST_PAGES = []

def printUsage():
	'Print script usage information'
	print '''python booknagar.py [-h] [-v] [--help] [--version] [-p pages] [-c chapters] -i input -o output

	-h, --help to view this help
	-v, --version to print program version number
	-p to select pages to work with
	-c to set first pages of chapters (separate with comma)
	-i to set input file
	-o to set output prefix
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
	opts, args = getopt.getopt(sys.argv[1:], 'hvp:c:i:o:', ['help', 'version'])
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
		elif opt == '-p':
			# parse pages:
			# 1-70,75,85-100 => [[1, 70], [75, 75], [85, 100]]
			pages = arg.split(',')
			for page_range in pages:
				page = page_range.split('-')
				if len(page) > 1:
					PAGES.append([int(page[0]), int(page[1])])
				else:
					PAGES.append([int(page[0]), int(page[0])])
		elif opt == '-c':
			# parse chapters first pages
			chapters = arg.split(',')
			for first_page in chapters:
				CHAPTERS_FIRST_PAGES.append(int(first_page))
		elif opt == '-i':
			INPUT_FILE = arg
		elif opt == '-o':
			OUTPUT_PREFIX = arg

if not INPUT_FILE:
	printUsage()
	sys.exit(2)
if not OUTPUT_PREFIX:
	printUsage()
	sys.exit(2)

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

if not PAGES:
	PAGES.append([1, 100]) # debug. count pages in ps file

PAGES.sort()
CHAPTERS_FIRST_PAGES.sort()

if CHAPTERS_FIRST_PAGES and CHAPTERS_FIRST_PAGES[0] != PAGES[0][0]:
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

# Page selection
# ==============

for chapter_ranges in PAGES:
	if chapter_ranges.count == 0:
		continue;

	chapter_command = '-p '
	pages_number = 0

	for chapter_pages in chapter_ranges:
		if chapter_pages[0] == chapter_pages[1]:
			chapter_command += '%d' % chapter_pages[0]
		else:
			chapter_command += '%d-%d' % (chapter_pages[0], chapter_pages[1])

		pages_number += chapter_pages[1] - chapter_pages[0] + 1
		chapter_command += ','

	pages_number += (4 - pages_number % 4) % 4
	chapter_number = PAGES.index(chapter_ranges)+1
	output_filename = '%s/%s_%d.ps' % (TEMP_DIR, OUTPUT_PREFIX, chapter_number)
	COMMAND_STRING += ' psselect %s %s | psbook > %s;' % (chapter_command[:-1], INPUT_FILE,
	                                                        output_filename)

	# Create bookletes
	current_booklete = 1
	pages_in_booklete = LISTS_IN_BOOKLETE * PAGES_ON_LIST

	input_filename = output_filename

	while (current_booklete-1) * pages_in_booklete < pages_number:
		min_page = pages_in_booklete * (current_booklete-1) + 1

		max_page = min_page + pages_in_booklete - 1
		if max_page > pages_number:
			max_page = pages_number
		# print 'Chapter: %d, pages: %d' % (chapter_number, pages_number)
		output_filename = '%s/%s_%s_%s.ps' % (OUTPUT_PREFIX, OUTPUT_PREFIX, chapter_number,
		                                      current_booklete)
		COMMAND_STRING += ' psselect -p %d-%d %s | psnup -2 -l -p a4 > %s;\n' % (min_page,
		                                                                       max_page,
		                                                                       input_filename,
		                                                                       output_filename)
		current_booklete += 1

# Cleaning
# ========

if temp_dir_created:
	os.rmdir(TEMP_DIR)

# Result
# ======

print COMMAND_STRING