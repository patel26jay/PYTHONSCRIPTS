#!/usr/bin/env python

import argparse
import getpass
import wget
import os
from pathlib import Path
from openpyxl import load_workbook

# Filename and URL
wb_file = 'Master%20Subnet%20Allocation-Store%20MPLS-2015-v1.xlsx'
svn_url = 'http://network/svn/network/amer/usa/stores/ip%20information/' + wb_file

# Columns
col_store = 0
col_city = 1
col_state = 2
col_subnet = 3

# Grab args/options
parser = argparse.ArgumentParser()
parser.add_argument('--store', type=str)
parser.add_argument('--subnet', type=str)
parser.add_argument('--city', type=str)
parser.add_argument('--state', type=str)
parser.add_argument('--update', action='store_true')
args = parser.parse_args()

def store_search(w, x, y, z):
  if w == x and y == z:
    print_store()

def print_store():
  print "\nStore " + str(row[col_store].value)
  print str(row[col_city].value) + ", " + str(row[col_state].value)
  print row[col_subnet].value + " /24"

def get_file():
  wget.download(svn_url)
  print("\nRe-run with search args to search newly downloaded file")

if args.update:
  os.remove(wb_file)
  get_file()

# Check for workbook, else download it
wb_path = Path('./' + wb_file)
if not wb_path.is_file():
  get_file()

# Read workbook, choose worksheet
wb = load_workbook(wb_file)

for region in range(1, 5):
  ws = wb['Region' + str(region)]
  for row in tuple(ws.rows):
    if args.store:
      store_search(str(row[col_store].value).lstrip("0"), str(args.store).lstrip("0"), None, None)
    if args.subnet:
      store_search(str(row[col_subnet].value), str(args.subnet), None, None)
    if args.city and args.state:
      store_search(str(row[col_city].value).lower(), str(args.city).lower(), str(row[col_state].value).lower(), str(args.state).lower())