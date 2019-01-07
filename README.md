# Nginx Upstream Monitor

This Docker container reads upstream information from an nginx-plus server using the API and posts a status message about it to a chat room.

The idea is that you run this container via a cronjob on a fixed schedule, giving you a very simple but powerful way of monitoring nginx.

Currently supported integrations are:

  - HipChat (both self-hosted and cloud)
  - Microsoft Teams
  - Slack

## Example usage

This example queries the nginx demo site, https://demo.nginx.com/

```
docker run -e NGINX_SERVER_URL=https://demo.nginx.com/ --rm -t kindredgroup/nginx-upstream-monitor
```

You probably want to create an enviroment file to make running the container easier:

```
# docker.env
ENVIRONMENT=PROD
NGINX_SERVER_URL=https://demo.nginx.com

USE_DIGEST_NOTIFICATIONS=1

HIPCHAT_ENABLED=1
HIPCHAT_SERVER=hipchat.example.com
HIPCHAT_TOKEN=x
HIPCHAT_ROOM_ID=123

TEAMS_ENABLED=1
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/xxx

SLACK_ENABLED=1
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy
SLACK_CHANNEL_NAME=#channel
```

and then run it like:

```
docker run --env-file=docker.env --rm -t kindredgroup/nginx-upstream-monitor
```

## Digst notifications

Instead of getting 1 line per notification you can also get a digest message that combines all the warnings and errors that were found in the current run. To use digest notifications add this variable to your config file:

```
USE_DIGEST_NOTIFICATIONS=1
```

## Supported integrations

You can use multiple integrations at the same time, but be aware that that will make your notifications run a bit slower.

[hipchat]: https://raw.githubusercontent.com/kindredgroup/nginx-upstream-monitor/master/docs/hipchat.png "HipChat Example notification"
[teams]: https://raw.githubusercontent.com/kindredgroup/nginx-upstream-monitor/master/docs/teams.png "Teams Example notification"

### HipChat

This uses the HipChat API v2 for room integrations. Required environment variables are:

  - HIPCHAT_ENABLED=1
  - HIPCHAT_SERVER=hipchat.example.com
  - HIPCHAT_TOKEN=x
  - HIPCHAT_ROOM_ID=123

![HipChat Example notification][hipchat]

### Microsoft Teams

Required environment variables are:

  - TEAMS_ENABLED=1
  - TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/xxx

Single notification:

![Teams Example notification][teams]

Digest notification:

TODO

### Slack

Required environment variables are:

  - SLACK_ENABLED=1
  - SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy
  - SLACK_CHANNEL_NAME=#channel

Single notification:

The Slack integration has not single notification support.

Digest notification:

TODO


## Acknowledgements

TODO

## License

The MIT License (MIT)

Copyright (c) 2018 Kindred People AB

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
