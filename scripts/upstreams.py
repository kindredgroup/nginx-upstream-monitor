#!/usr/bin/env python
#
# My first python 3 script after using 2.7 for years. Please forgive any
# newbie mistakes found in here.

import os
import json
import urllib.request
import urllib.parse

from integrations.hipchat import *
from integrations.teams import *

def send_notification(component, message, status, link_url, total_upstreams, healthy_upstreams):

  send_hipchat = os.getenv('HIPCHAT_ENABLED', 0)
  send_teams   = os.getenv('TEAMS_ENABLED', 0)
  send_slack   = os.getenv('SLACK_ENABLED', 0)

  # We read configuration as environment variables to make it work smooth with Docker
  ENVIRONMENT = os.getenv('ENVIRONMENT', 'PROD')

  HIPCHAT_SERVER  = os.getenv('HIPCHAT_SERVER', 'api.hipchat.com')
  HIPCHAT_TOKEN   = os.getenv('HIPCHAT_TOKEN', '')
  HIPCHAT_ROOM_ID = os.getenv('HIPCHAT_ROOM_ID', '')

  TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL', '')

  SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')

  # HipChat is hardcoded ON right now
  if send_hipchat:
    print ("Sending HipChat notification...")

    try:
      hipchat_notify(host=HIPCHAT_SERVER, token=HIPCHAT_TOKEN, room=HIPCHAT_ROOM_ID,
                     message=message, status=status, component=component, link_url=link_url,
                     environment=ENVIRONMENT, total_upstreams=total_upstreams, healthy_upstreams=healthy_upstreams)
    except Exception as e:
      msg = "[ERROR] HipChat notify failed: '{0}'".format(e)
      print(msg, file=sys.stderr)

  # Microsoft Teams
  if send_teams:
    print ("Sending Teams notification...")

    try:
      teams_notify(webhook=TEAMS_WEBHOOK_URL, message=message, status=status,
                   component=component, link_url=link_url,
                   environment=ENVIRONMENT, total_upstreams=total_upstreams,
                   healthy_upstreams=healthy_upstreams)
    except Exception as e:
      msg = "[ERROR] Teams notify failed: '{0}'".format(e)
      print(msg, file=sys.stderr)


  # Slack
  if send_slack:
    print ("Sending Slack notification...")


def check_upstreams(base_url):

  print ("### nginx-plus upstream monitor check")
  print ("")

  data_url = base_url + '/api/3/http/upstreams/'
  link_url = base_url + '/dashboard.html#upstreams'

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
              print ("   -> Peer is marked as down, ignorning status")

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
              message = "No healthy peers found, component is down!"
              status = "ERROR"

            elif unhealthy > 0:
              status = "WARNING"
              message = "Some peers are unhealthy, active HTTP health check failed"

            elif unavail > 0:
              status = "WARNING"
              message = "Some peers are unavailable, passive TCP server check failed"

            else:
              status = "INFO"
              message = "All servers look good, not sending a message"

          # We are done with processing, show a result and send it to the integrations
          print (status + ": " + message)
          if status != 'INFO':
            send_notification(component=upstream, message=message, status=status, link_url=link_url, total_upstreams=total, healthy_upstreams=up)

    print ("")

if __name__ == "__main__":
  import sys
  check_upstreams(sys.argv[1])
