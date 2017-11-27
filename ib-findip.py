#!/usr/bin/env python

from __future__ import print_function
from pyinfoblox import InfobloxWAPI
import urllib3
import getpass
urllib3.disable_warnings()

ibUser = raw_input('User: ')
ibPass = getpass.getpass('Password: ')

infoblox = InfobloxWAPI(
    username=ibUser,
    password=ibPass,
    wapi='https://ipam/wapi/v2.2.2/'
)

print("\n\nPaste MAC addresses in xx:xx:xx:xx:xx:xx format and then Ctrl+D: ")
macs = []
try:
    while True:
        macs.append(raw_input())
except EOFError:
    pass

print("\n\nSearching Infoblox for mapped IPs:")

for mac in macs:
    macmatch = infoblox.search.get(search_string=mac)
    if not macmatch:
        print("No result for %s" % mac)
        continue

    if not 'ipv4addr' in macmatch[0].keys():
        if not 'ip_address' in macmatch[0].keys():
            print("Result for %s is non-readable" % mac)
        else:
            print("%s - %s" % (mac,macmatch[0]['ip_address']))
    else:
        print("%s - %s" % (mac,macmatch[0]['ipv4addr']))
