#!/usr/bin/python
#
# example call:
#
# ./downloader http://downloads.bremen.freifunk.net/firmware/
#

import sys
import subprocess


class Downloader:
    def __init__(self, base_url):
        self.base_url = base_url

    def download(self):
        command = ["wget"]

        # -N don't re-retrieve files unless newer than local
        command.extend(["-N"])

        # recursively
        command.extend(["-r"])

        # No parents
        command.extend(["-np"])

        # Load firmware and manifests only
        command.extend(["-A", ".bin,.image,.manifest"])

        # don't create the subdirectory downloads
        command.extend(["-nH"])

        # don't create the sub directory firmware/
        command.extend(["--cut-dirs=1"])

        # ignore the remote directory nightly, its just a symlink
        command.extend(["-X", "/firmware/nightly"])

        # the url
        command.extend(self.base_url)

        # Start the subprocess
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        try:
            # write to stdin
            process.communicate(input=self.lines)
        except:
            process.kill()
            process.wait()
            raise

l = Downloader(sys.argv[1])
l.download()
print("Download finished")
