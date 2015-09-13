#!/usr/bin/python
#
# example call:
#
# ./downloader http://downloads.bremen.freifunk.net/firmware/
#

import sys
import subprocess


class Downloader:
    def __init__(self, base_url, output_dir=""):
        self.base_url = base_url
        self.output_dir = output_dir

    def download(self):
        command = ["wget"]

        # -P Set directory prefix to prefix. The directory
        # prefix is the directory where all other files
        # and sub-directories will be saved to, i.e.
        # the top of the retrieval tree.
        # The default is . (the current directory).
        if self.output_dir != "":
            command.extend(["-P", self.output_dir])

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
        command.extend([self.base_url])

        # Start the subprocess
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.wait()

l = Downloader(sys.argv[1])
l.download()
print("Download finished")
