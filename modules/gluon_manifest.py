#!/usr/bin/python
#
# example call:
#
# ./gluon-manifest stable.manifest site.conf
#

import subprocess
from slpp import slpp as lua


class Manifest:
    NAME = 0
    VERSION = 1
    HASH_SUM = 2
    FILE_NAME = 3

    def __init__(self, path):
        self.path = path
        self.state = 'start'
        self.lines = ''  # lines to verify
        self.firmwares = []
        self.signatures = []
        self.vars = dict()
        self._parse()

    # returns the current branch
    def branch(self):
        return self.vars["BRANCH"]

    # return whether enough signatures are valid
    def verify_signatures(self, site_conf):
        config = self.site_conf(site_conf)['autoupdater']['branches'][self.branch()]
        command = ["ecdsaverify", "-n", str(config['good_signatures'])]

        # Add public keys
        for key in config['pubkeys']:
            command.extend(["-p", key])

        # Add signatures
        for sig in self.signatures:
            command.extend(["-s", sig])

        # Start the subprocess
        ecdsa_process = subprocess.Popen(command, stdin=subprocess.PIPE)
        try:
            # write to stdin
            ecdsa_process.communicate(input=self.lines)
        except:
            ecdsa_process.kill()
            ecdsa_process.wait()
            raise
        return ecdsa_process.poll() == 0

    # the parsed site.conf
    def site_conf(self, site_conf):
        with open(site_conf, 'r') as f:
            return lua.decode(f.read())

    def _parse(self):
        with open(self.path, 'r') as f:
            for line in f:
                # parse the line
                getattr(self, "_" + self.state)(line.strip())

                # data do verify
                if self.state != "signatures":
                    self.lines += line

    def _start(self, line):
        if line == "":
            self.state = "files"
        else:
            k, v = line.split("=", 2)
            self.vars[k] = v

    def _files(self, line):
        if line == "---":
            self.state = "signatures"
        else:
            self.firmwares.append(line.split(" "))

    def _signatures(self, line):
        self.signatures.append(line)