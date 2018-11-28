#!/usr/bin/env python
#

from __future__ import print_function

import requests
import sys
import json
import datetime

teams_sections = []

def flush_teams_queue(webhook_url, environment='unknown', link_url=''):

  count = len(teams_sections)

  if count == 0:
    print ("There are no notifications to send.")
    return

  payload = {
    "@type": "MessageCard",
    "@context": "https://schema.org/extensions",
    "summary": " There were problems",
    "sections": teams_sections
  }

  print(payload)

  # Send the actual call to the HipChat server
  r = requests.post(webhook_url, json=payload)
  r.raise_for_status()


# Add a notification to the queue
def teams_queue(component, message, status, total_upstreams, healthy_upstreams):

  now = datetime.datetime.now()
  date = now.strftime("%Y-%m-%d %H:%M:%S")

  # TODO: Don't hotlink to someone else's image, host our own somewhere static
  status_image = "http://www.keysigns.co.uk/images/hazard-warning-safety-signs-p1254-38488_zoom.jpg"
  if status == 'error':
    status_image = "https://www.changefactory.com.au/wp-content/uploads/2010/09/bigstock-Vector-Error-Icon-66246010.jpg"

  section = {
    "startGroup": "true",
    "title": "{}: {}".format(status, component),
    "activityImage": status_image,
    "activityTitle": message,
    "activitySubTitle": date,
    "facts": [
      {
        "name": "Component:",
        "value": component
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
  }

  teams_sections.append(section)


def teams_notify(webhook, message, link_url='http://www.example.com', component='unknown', status='unknown', total_upstreams=0, healthy_upstreams=0, environment='PROD'):

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    # TODO: Don't hotlink to someone else's image, host our own somewhere static
    status_image = "http://www.keysigns.co.uk/images/hazard-warning-safety-signs-p1254-38488_zoom.jpg"
    if status == 'error':
      status_image = "https://www.changefactory.com.au/wp-content/uploads/2010/09/bigstock-Vector-Error-Icon-66246010.jpg"

    # See: https://docs.microsoft.com/en-us/outlook/actionable-messages/message-card-reference
    section = {
      "startGroup": "true",
      "title": "{}: {}".format(status, component),
      "activityImage": status_image,
      "activityTitle": message,
      "activitySubTitle": date,
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

