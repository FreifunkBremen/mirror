#!/usr/bin/env python

import os
import datetime
from dateutil import parser
import urllib2
import logging

class Downloader:
    log = logging.getLogger('mirror')

    def __init__(self, site_conf_url):
        self.DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        # https://raw.githubusercontent.com/FreifunkBremen/gluon-site-ffhb/master/site.conf
        self.SITE_CONF = site_conf_url

    def download(self, url, destination):
        request = urllib2.Request(url)

        # Get modification time
        if os.path.isfile(destination):
            unix = int(os.path.getmtime(destination))
            request.headers["if-modified-since"] = datetime.datetime.fromtimestamp(unix).strftime(self.DATE_FORMAT)

        try:
            opener = urllib2.build_opener()
            stream = opener.open(request)
            self.log.info("%s was downloaded to %s.", url, destination)
        except urllib2.HTTPError, e:
            if e.code == 304:
                # Not modified
                self.log.debug("%s is up to date.", destination)
                return False
            raise

        # Write to file
        with open(destination, 'w') as f:
            f.write(stream.read())

        # Set modified
        if 'last-modified' in stream.headers:
            modified = parser.parse(stream.headers["last-modified"])
            unix = int(modified.strftime("%s"))
            os.utime(destination, (unix, unix))
        else:
            self.log.debug('stream does not contain last-modified')

        # File modified
        return True

    def get_site_conf(self, destination):
        self.download(self.SITE_CONF, destination)
