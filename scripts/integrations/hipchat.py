#!/usr/bin/env python
#
# Taken from https://gist.github.com/bdclark/4bc8ed06643e077fa620
#   ... and modified quite a bit.

from __future__ import print_function

import requests
import sys
import json

def hipchat_notify(token, room, message, color='yellow', link_url='http://www.example.com',
                   format='text', host='api.hipchat.com', component='unknown',
                   status='unknown', status_style='lozenge-current',
                   total_upstreams=0, healthy_upstreams=0, environment='PROD'):

    if len(message) > 10000:
        raise ValueError('Message too long')

    if format not in ['text', 'html']:
        raise ValueError("Invalid message format '{0}'".format(format))

    if color not in ['yellow', 'green', 'red', 'purple', 'gray', 'random']:
        raise ValueError("Invalid color {0}".format(color))

    url = "https://{0}/v2/room/{1}/notification".format(host, room)
    headers = {'Authorization': 'Bearer ' + token}

    # A HipChat application card
    card = {
        'style': 'application',
        'id': '1',
        'format': 'compact',
        'url': link_url,
        'title': "{0} - {1}".format(component,message),
        'attributes': [
            {
                'label': 'Status',
                'value': {'label': status, 'style': status_style}
            },
            {
                'label': 'Environment',
                'value': {'label': environment}
            },
            {
                'label': 'Total upstreams',
                'value': {'label': "{}".format(total_upstreams)}
            },
            {
                'label': 'Healthy upstreams',
                'value': {'label': "{}".format(healthy_upstreams)}
            }
        ]
    }

    # The generic HipChat payload. This is also the information shown
    # when the card is not rendered e.g. on mobile devices.
    payload = {
        'form': 'Nginx Upstream Monitor',
        'message': "{0} - {1}".format(component,message),
        'notify': 'true',
        'message_format': format,
        'color': color,
        'card': card
    }

#    print(payload)

    # Send the actual call to the HipChat server
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
