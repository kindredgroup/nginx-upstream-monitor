# Nginx Upstream Monitor

This Docker container reads upstream information from an nginx-plus server using the API and posts a status message about it to a chat room. Currently it only displays information messages on the console but more integrations will be added soon.

## Example usage

This example queries the nginx demo site, https://demo.nginx.com/

```
docker run -e NGINX_SERVER_URL=https://demo.nginx.com/ --rm -t kindredgroup/nginx-upstream-monitor
```

You probably want to create an enviroment file to make running the container easier:

```
# docker.env
ENVIRONMENT=PROD

HIPCHAT_ENABLED=1
HIPCHAT_SERVER=hipchat.example.com
HIPCHAT_TOKEN=x
HIPCHAT_ROOM_ID=123

TEAMS_ENABLED=1
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/xxx
```

and then run it like:

```
docker run --env-file=docker.env --rm -t kindredgroup/nginx-upstream-monitor
```

## Supported integrations

  - HipChat on-premise
  - Microsoft Teams

## Upcoming integrations

  - Slack

## Acknowledgement

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
