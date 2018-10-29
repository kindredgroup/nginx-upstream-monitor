#!/usr/bin/env python
#

from __future__ import print_function

import requests
import sys
import json
import datetime

def teams_notify(webhook, message, link_url='http://www.example.com', component='unknown', status='unknown', total_upstreams=0, healthy_upstreams=0, environment='PROD'):

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    # TODO: Don't hotlink to someone else's image, host our own somewhere static
    status_image = "http://www.keysigns.co.uk/images/hazard-warning-safety-signs-p1254-38488_zoom.jpg"
    if status == 'error':
      status_image = "https://www.changefactory.com.au/wp-content/uploads/2010/09/bigstock-Vector-Error-Icon-66246010.jpg"

    # See: https://docs.microsoft.com/en-us/outlook/actionable-messages/message-card-reference

    payload = {
      "@type": "MessageCard",
      "@context": "https://schema.org/extensions",
      "summary": "{0} - {1}".format(component,message),
      "sections": [
        {
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
      ]
    }

    # print(payload)

    r = requests.post(webhook, json=payload)
    r.raise_for_status()

