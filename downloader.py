#!/usr/bin/python


import os
import datetime
from dateutil import parser
import urllib2


class Downloader:
    def download(self, url, destination):
        request = urllib2.Request(url)

        # Get modification time
        if os.path.isfile(destination):
            unix = int(os.path.getmtime(destination))
            request.headers["if-modified-since"] = datetime.datetime.fromtimestamp(unix).strftime('%a, %d %b %Y %H:%M:%S GMT')

        try:
            opener = urllib2.build_opener()
            stream = opener.open(request)
            print(str.format("{0} was downloaded to {1}.", url, destination))
        except urllib2.HTTPError, e:
            if e.code == 304:
                # Not modified
                print(str.format("{0} is up to date.", destination))
                return False
            raise


        # Write to file
        with open(destination, 'w') as f:
            f.write(stream.read())

        # Set modified
        modified = parser.parse(stream.headers["last-modified"])
        unix = int(modified.strftime("%s"))
        os.utime(destination, (unix, unix))

        # File modified
        return True
