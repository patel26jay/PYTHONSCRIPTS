#!/usr/bin/env python
import orionsdk
import urllib3
import sys
import re
urllib3.disable_warnings()

if len(sys.argv) < 2:
  print("no argument given")
  exit()

config_id = ""
rtr = str(sys.argv[1])

# Login
swis = orionsdk.SwisClient("netmon.ultainc.lcl", "configdl", "Ulta123$")

# Get configID for latest running config, using search config function
try:
  config_id = str(swis.invoke("Cirrus.ConfigArchive", "ConfigSearch", rtr, "running", "", False, True)[0])
except:
  print("no match for given hostname")
  exit()

# Grab config
config = swis.query("SELECT Config FROM Cirrus.ConfigArchive WHERE ConfigID=" + config_id)

# Regex to catch local AS and remote AS
p1 = re.compile(".*(router bgp [0-9]+)\r.*")
p2 = re.compile(".*(neighbor [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ remote-as [0-9]+)\r")

# Search configs using regex
as_self = p1.search(config['results'][0]['Config']).group(1)
as_remote = p2.search(config['results'][0]['Config']).group(1)

# Print matching output
print("\nLocal AS statement:\n" + as_self)
print("\nRemote AS statement:\n" + as_remote)
