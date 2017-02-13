#!/usr/bin/python
#
# example call:
#
# ./mirror http://downloads.bremen.freifunk.net/firmware/
#

import hashlib
import os
import shutil

from modules.downloader import Downloader
from modules.gluon_manifest import Manifest

# import sys
import argparse
import logging


class Mirror:
    SYSUPGRADE = "sysupgrade"
    MANIFEST_EXT = ".manifest"
    BUFFER_SIZE = 4096
    DEBUG = False

    log = logging.getLogger('mirror')
    log.setLevel(logging.DEBUG)

    log_file = logging.FileHandler('mirror.log')
    log_file.setLevel(logging.INFO)

    log_console = logging.StreamHandler()
    log_console.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    log_file.setFormatter(formatter)
    log_console.setFormatter(formatter)

    log.addHandler(log_file)
    log.addHandler(log_console)

    def __init__(self, url, site_conf, destination):
        self.url = url
        self.working_directory = destination
        self.downloader = Downloader()
        self.branches = ["stable", "testing"]
        self.site_conf = site_conf

    def create(self):
        self._prepare_directories()

        self.log.info("Get site conf...")
        self.downloader.get_site_conf('site.conf')

        for b in self.branches:
            manifest = self.get_manifest(b)

            if manifest is None:
                continue

            for f in manifest.firmwares:
                image_path = self.get_image(f, manifest)

                if image_path is None:
                    continue

                hash_sum = self.create_sha512(image_path)

                if not hash_sum == f[manifest.HASH_SUM]:
                    self.log.error("Hash does not match, deleting file...")
                    os.remove(image_path)

    def get_manifest(self, b):
        manifest_url = self.get_manifest_url(b)
        manifest_path = self.get_manifest_path(b)

        self.log.info("Downloading %s%s", b, self.MANIFEST_EXT)

        if not self.downloader.download(manifest_url, manifest_path):
            self.log.info("The manifest has same timestamp as the local file. Nothing to do.")
            return None

        manifest = Manifest(manifest_path)

        if not manifest.verify_signatures(os.path.abspath("site.conf")):
            self.log.error("Signature of manifest for branch %s is not valid. Nothing will be downloaded.", b)
            return None

        return manifest

    def get_image(self, f, manifest):
        b = str.lower(manifest.vars["BRANCH"])
        file_url = self.get_file_url(b, f[manifest.FILE_NAME])
        file_path = self.get_file_path(b, f[manifest.FILE_NAME])
        if self.downloader.download(file_url, file_path):
            return file_path

        return None

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

    def create_sha512(self, file_name):
        sha = hashlib.sha512()
        with open(file_name) as f:
            for chunk in iter(lambda: f.read(self.BUFFER_SIZE), ""):
                sha.update(chunk)
        return sha.hexdigest()

    def _prepare_directories(self):
        if self.DEBUG:
            if os.path.exists(self.working_directory):
                shutil.rmtree(self.working_directory)

        for b in self.branches:
            path = str.format("{0}/{1}/{2}", self.working_directory, b, self.SYSUPGRADE)
            if not os.path.exists(path):
                os.makedirs(path)


parser = argparse.ArgumentParser(description='Create a sysupgrade freifunk mirror.')
parser.add_argument('-u', '--url', type=str, help='Source url of the mirror (http://...)', required=True)
parser.add_argument('-s', '--site-conf', type=str, default='site.conf', help='Path to site.conf, default is ./site.conf')
parser.add_argument('-r', '--root', type=str, default='mirror', help='Root directory of the mirror. Default is ./mirror')

# were taken implicitly from sys.argv
args = parser.parse_args()

Mirror(args.url, args.site_conf, args.root).create()
