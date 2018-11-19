#!/usr/bin/env python
#
# ./download.py http://www.example.com/ index.html
#

import sys
import os
import datetime
from dateutil import parser
import urllib2

def download(url, dest):
  request  = urllib2.Request(url)

  # Get modification time
  if os.path.isfile(dest):
    unix = int(os.path.getmtime(dest))
    request.headers["if-modified-since"] = datetime.datetime.fromtimestamp(unix).strftime('%a, %d %b %Y %H:%M:%S GMT')

  try:
    opener = urllib2.build_opener()
    stream = opener.open(request)
  except urllib2.HTTPError, e:
    if e.code==304:
      # Not modified
      return False
    raise

  # Write to file
  with open(dest, 'w') as f:
    f.write(stream.read())

  # Set modified
  modified = parser.parse(stream.headers["last-modified"])
  unix     = int(modified.strftime("%s"))
  os.utime(dest, (unix, unix))

  # File modified
  return True

if download(sys.argv[1], sys.argv[2]):
  print "modified"
else:
  print "not modified"
