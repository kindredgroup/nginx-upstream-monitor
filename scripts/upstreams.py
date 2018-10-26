#!/usr/bin/env python
#
# My first python 3 script after using 2.7 for years. Please forgive any
# newbie mistakes found in here.

import json
import urllib.request
import urllib.parse
import os
import sys

print ("### nginx-plus upstream monitor check")
print ("")

base_url = sys.argv[1]
data_url = base_url + '/api/3/http/upstreams/'
link_url = base_url +'/dashboard.html#upstreams'

print ("Nginx API URL:                    {}".format(data_url))
print ("Nginx Public URL (used in links): {}".format(link_url))
print ("")

f = urllib.request.urlopen(data_url)
loaded_json = json.loads(f.read().decode('utf-8'))

for upstream in loaded_json:
  print("Upstream: {}".format(upstream))

  for item in loaded_json[upstream]:

    if item == "peers":
      if len(loaded_json[upstream][item]) == 0:
        print ("No upstreams found.")

      else:
        up = unhealthy = unavail = total = 0
        for peer in loaded_json[upstream][item]:
          state  = peer["state"]
          name   = peer["name"]
          server = peer["server"]
          print(" - %-21s %10s" % (server, state))

          if state == "down":
            print ("Ignoring: Peer is marked as down, ignorning status")

          elif state == "up":
            total += 1
            up += 1

          elif state == "unhealthy":
            total += 1
            unhealthy += 1

          elif state == "unavail":
            total += 1
            unavail += 1

        if total == 0:
          print ("Ignoring: Upstream has no valid members, ignorning any status.")

        elif total == 1:
          print ("Ignoring: Upstream has only one member, ignoring any status since this is not an HA setup.")

        # At this point we consider the upstream to be a real one, which peers
        # we actually need to look at for a status.
        elif total > 1:

          if up == 0:
            type = "ERROR"
            message = "No healthy peers found, component is down!"

          elif unhealthy > 0:
            type = "WARNING"
            message = "Some peers are unhealthy, active HTTP health check failed."

          elif unavail > 0:
            type = "WARNING"
            message = "Some peers are unavailable, passive TCP server check failed."

          else:
            type = "INFO"
            message = "All servers look good, not sending a message."

        # We are done with processing, show a result and send it to the integrations
        print (type + ": " + message)

        # TODO: Add calls to integrations here


  print ("")
print ("# Program finished!")
print ("")
