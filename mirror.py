#!/usr/bin/python
#
# example call:
#
# ./mirror http://downloads.bremen.freifunk.net/firmware/
#

from downloader import Downloader
from gluon_manifest import Manifest
import sys
import os
import shutil


class Mirror:
    SYSUPGRADE = "sysupgrade"
    MANIFEST_EXT = ".manifest"

    def __init__(self, url, destination="work"):
        self.url = url
        self.working_directory = destination
        self.downloader = Downloader()
        self.branches = ["stable", "testing"]

    def create(self):
        self._prepare_directories()
        self.get_manifests()

    def get_manifest_url(self, branch_name):
        return str.format("{0}/{1}/{2}/{1}{3}",
                          self.url, branch_name, self.SYSUPGRADE, self.MANIFEST_EXT)

    def get_manifest_path(self, branch_name):
        return os.path.abspath(str.format("{0}/{1}/{2}/{1}{3}",
                                          self.working_directory, branch_name, self.SYSUPGRADE, self.MANIFEST_EXT))

    def get_file_url(self, branch_name, file_name):
        return str.format("{1}/{0}/{3}/{2}",
                          branch_name, self.url, file_name, self.SYSUPGRADE)

    def get_file_path(self, branch_name, file_name):
        return os.path.abspath(str.format("{1}/{0}/{3}/{2}",
                                          branch_name, self.working_directory, file_name, self.SYSUPGRADE))

    def get_manifests(self):
        for b in self.branches:
            manifest_url = self.get_manifest_url(b)
            manifest_path = self.get_manifest_path(b)

            print(str.format("Downloading {0}{1}", b, self.MANIFEST_EXT))
<<<<<<< HEAD

            if not self.downloader.download(manifest_url, manifest_path):
                print("The manifest has same timestamp as the local file. Nothing to do.")
                continue
=======
            self.downloader.download(manifest_url, manifest_path)
>>>>>>> 6499407a0b036df0c3dea59a99e9fb0e2144b2d9

            manifest = Manifest(manifest_path)

            if not manifest.verify(os.path.abspath("site.conf")):
                print(str.format("Signature of manifest for branch {0} is not valid. Nothing will be downloaded.", b))
                continue

            print(str.format("Signature of manifest for branch {0} is valid. Begin download", b))

            self.get_images(manifest)

    def get_images(self, manifest):
        b = str.lower(manifest.vars["BRANCH"])
        for f in manifest.firmwares:
            print(str.format("Downloading {0}", f[manifest.NAME]))
            file_url = self.get_file_url(b, f[manifest.FILE_NAME])
            file_path = self.get_file_path(b, f[manifest.FILE_NAME])
            self.downloader.download(file_url, file_path)

    def _prepare_directories(self):
        if os.path.exists(self.working_directory):
            shutil.rmtree(self.working_directory)

        os.mkdir(self.working_directory)

        for b in self.branches:
            path = str.format("{0}/{1}/{2}", self.working_directory, b, self.SYSUPGRADE)
            os.makedirs(path)

<<<<<<< HEAD
if len(sys.argv) > 2:
=======
if len(sys.argv) >= 2:
>>>>>>> 6499407a0b036df0c3dea59a99e9fb0e2144b2d9
    mirror = Mirror(sys.argv[1], sys.argv[2])
else:
    mirror = Mirror(sys.argv[1])
mirror.create()
