#!/usr/bin/env python
#
# See: https://docs.microsoft.com/en-us/outlook/actionable-messages/message-card-reference

from __future__ import print_function

import requests
import sys
import json

teams_sections = []

def flush_teams_queue(webhook_url, environment='unknown', link_url=''):

  count = len(teams_sections)

  if count == 0:
    print ("There are no notifications to send.")
    return

  payload = {
    "@type": "MessageCard",
    "@context": "https://schema.org/extensions",
    "title": "We found {0} {2} on the *{1}* environment:".format(count, environment, "problem" if count < 2 else "problems"),
    "summary": "Nginx Upstream Monitor has found {0} problems on the *{1}* environment".format(count, environment),
    "sections": teams_sections
  }

  print(payload)

  # Send the actual call to the HipChat server
  r = requests.post(webhook_url, json=payload)
  r.raise_for_status()


# Add a notification to the queue
def teams_queue(component, message, status, total_upstreams, healthy_upstreams):

  status_image = "https://www.karelbemelmans.com/images/teams-status-images/warning.jpg"
  if status == 'ERROR':
    status_image = "https://www.karelbemelmans.com/images/teams-status-images/error.jpg"

  section = {
    "startGroup": "true",
    "activityImage": status_image,
    "activityTitle": "{}: {} - {}".format(status, component, message),
    "activitySubTitle": "Total upstreams: {0} - Healthy upstream: {1}".format(total_upstreams, healthy_upstreams)
  }

  teams_sections.append(section)


def teams_notify(webhook, message, link_url='http://www.example.com', component='unknown', status='unknown', total_upstreams=0, healthy_upstreams=0, environment='PROD'):

  status_image = "https://www.karelbemelmans.com/images/teams-status-images/warning.jpg"
  if status == 'ERROR':
    status_image = "https://www.karelbemelmans.com/images/teams-status-images/error.jpg"

  section = {
    "startGroup": "true",
    "title": "{}: {}".format(status, component),
    "activityImage": status_image,
    "activityTitle": message,
    "facts": [
      {
        "name": "Environment:",
        "value": environment
      },
      {
        "name": "Total upstreams:",
        "value": total_upstreams
      },
      {
        "name": "Healthy upstreams:",
        "value": healthy_upstreams
      }
    ]
  },
  {
    "potentialAction": [
      {
        "@type": "OpenURI",
        "name": "View status page",
        "targets": [
          { "os": "default", "uri": link_url },
        ]
      }
    ]
  }

  payload = {
    "@type": "MessageCard",
    "@context": "https://schema.org/extensions",
    "summary": "{0} - {1}".format(component,message),
    "sections": [ sections ]
  }

  # print(payload)

  r = requests.post(webhook, json=payload)
  r.raise_for_status()

