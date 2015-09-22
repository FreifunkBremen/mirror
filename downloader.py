#!/usr/bin/python
#
# ./download.py http://www.example.com/ index.html
#


import sys
import os
import datetime
from dateutil import parser
import urllib2


class Downloader:
    def download(self, url, destination):
        request = urllib2.Request(url)

        print(str.format("From {0}", url))
        print(str.format("To {0}", destination))

        # Get modification time
        if os.path.isfile(destination):
            unix = int(os.path.getmtime(destination))
            request.headers["if-modified-since"] = datetime.datetime.fromtimestamp(unix).strftime('%a, %d %b %Y %H:%M:%S GMT')

        try:
            opener = urllib2.build_opener()
            stream = opener.open(request)
        except urllib2.HTTPError, e:
            if e.code == 304:
                # Not modified
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

# if download(sys.argv[1], sys.argv[2]):
#     print "modified"
# else:
#     print "not modified"


# #!/usr/bin/python
# #
# # example call:
# #
# # ./downloader http://downloads.bremen.freifunk.net/firmware/
# #
# 
# import sys
# import subprocess
# 
# 
# class Downloader:
#         def __init__(self, base_url, output_dir=""):
#                 self.base_url = base_url
#                 self.output_dir = output_dir
# 
#         def download_manifests(self):
#                 command = ["wget"]
# 
#                 # -P Set directory prefix to prefix. The directory
#                 # prefix is the directory where all other files
#                 # and sub-directories will be saved to, i.e.
#                 # the top of the retrieval tree.
#                 # The default is . (the current directory).
#                 if self.output_dir != "":
#                         command.extend(["-P", self.output_dir])
# 
#                 # -N don't re-retrieve files unless newer than local
#                 command.extend(["-N"])
# 
#                 # recursively
#                 command.extend(["-r"])
# 
#                 # No parents
#                 command.extend(["-np"])
# 
#                 # Don't scream
#                 command.extend(["--no-verbose"])
# 
#                 # Load firmware and manifests only
#                 command.extend(["-A", ".manifest"])
# 
#                 # don't create the subdirectory downloads
#                 command.extend(["-nH"])
# 
#                 # don't create the sub directory firmware/
#                 command.extend(["--cut-dirs=1"])
# 
#                 # ignore the remote directory nightly, its just a symlink
#                 command.extend(["-X", "/firmware/nightly"])
# 
#                 # the url
#                 command.extend([self.base_url])
# 
#                 # Start the subprocess
#                 process = subprocess.Popen(command, stdin=subprocess.PIPE)
#                 process.wait()
# 
#         def download_all(self):
#                 command = ["wget"]
# 
#                 # -P Set directory prefix to prefix. The directory
#                 # prefix is the directory where all other files
#                 # and sub-directories will be saved to, i.e.
#                 # the top of the retrieval tree.
#                 # The default is . (the current directory).
#                 if self.output_dir != "":
#                         command.extend(["-P", self.output_dir])
# 
#                 # -N don't re-retrieve files unless newer than local
#                 command.extend(["-N"])
# 
#                 # recursively
#                 command.extend(["-r"])
# 
#                 # No parents
#                 command.extend(["-np"])
# 
#                 # Don't scream
#                 command.extend(["--no-verbose"])
# 
#                 # Load firmware and manifests only
#                 command.extend(["-A", ".bin,.image,.manifest"])
# 
#                 # don't create the subdirectory downloads
#                 command.extend(["-nH"])
# 
#                 # don't create the sub directory firmware/
#                 command.extend(["--cut-dirs=1"])
# 
#                 # ignore the remote directory nightly, its just a symlink
#                 command.extend(["-X", "/firmware/nightly"])
# 
#                 # the url
#                 command.extend([self.base_url])
# 
#                 # Start the subprocess
#                 process = subprocess.Popen(command, stdin=subprocess.PIPE)
#                 process.wait()
# 
# #l = Downloader(sys.argv[1])
# #l.download()
# #print("Download finished")
