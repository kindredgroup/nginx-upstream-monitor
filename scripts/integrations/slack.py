#!/usr/bin/env python
#
# Taken from https://gist.github.com/bdclark/4bc8ed06643e077fa620
#   ... and modified quite a bit.
#

from __future__ import print_function

import requests
import sys
import json
import datetime

def slack_notify(webhook_url, channel, message, link_url='http://www.example.com',
                   format='text', host='api.hipchat.com', component='unknown',
                   status='unknown', status_style='lozenge-current',
                   total_upstreams=0, healthy_upstreams=0, environment='PROD'):

    color = 'warning'
    if status == 'error':
      color = 'danger'

    if len(message) > 10000:
        raise ValueError('Message too long')

    if format not in ['text', 'html']:
        raise ValueError("Invalid message format '{0}'".format(format))

    # See: https://api.slack.com/docs/message-attachments
    attachment = {
        "color": color,
        "title": "Upstream: {0}".format(component),
        "title_link": link_url,
        "text": message,
        "fields": [
          {
            "title": "Type:",
            "value": status,
            "short": True
          },
          {
            "title": "Environment:",
            "value": environment,
            "short": True
          },
          {
            "title": "Total upstreams:",
            "value": total_upstreams,
            "short": True
          },
          {
            "title": "Healthy upstreams:",
            "value": healthy_upstreams,
            "short": True
          }
        ],
    }

    payload = {
        'channel': channel,
        'username': 'Nginx Upstream Monitor',
        'text': "Nginx Upstream Monitor has found a problem!",
        "attachments": [
            attachment
        ]
    }

    print(payload)

    # Send the actual call to the HipChat server
    r = requests.post(webhook_url, json=payload)
    r.raise_for_status()
