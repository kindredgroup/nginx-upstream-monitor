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

slack_attachments = []

def flush_slack_queue(webhook_url, channel, environment='unknown'):

  count = len(slack_attachments)

  if count == 0:
    print ("There are no notifications to send.")
    return

  payload = {
      'channel': channel,
      'username': 'Nginx Upstream Monitor',
      'text': "Nginx Upstream Monitor has found {0} problems on the {1} environment".format(count, environment),
      "attachments": slack_attachments
  }

  print(payload)

  # Send the actual call to the HipChat server
  r = requests.post(webhook_url, json=payload)
  r.raise_for_status()


# Add a notification to the queue
def slack_queue(component, message, status, total_upstreams, healthy_upstreams, link_url=''):

  color = 'warning'
  if status == 'error':
    color = 'danger'

  attachment = {
    "color": color,
    "title": "Component: {0}".format(component),
    "title_link": link_url,
    "text": "{0}\n*Total upstreams*: {1} - *Healthy upstreams*: {2}".format(message, total_upstreams, healthy_upstreams)
  }

  slack_attachments.append(attachment)


# Send a single, complete message to Slack
def slack_notify(webhook_url, channel, message, link_url='http://www.example.com', format='text', component='unknown', status='unknown', total_upstreams=0, healthy_upstreams=0, environment='PROD'):

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
        "title": "{0} - {1}".format(environment, component),
        "title_link": link_url,
        "text": message,
        "fields": [
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

    # Send the actual call to the HipChat server
    r = requests.post(webhook_url, json=payload)
    r.raise_for_status()
