#!/usr/bin/python

import sys

class Manifest:
    def __init__(self, path):
        self.state      = 'start'
        self.entries    = []
        self.signatures = []
        self.vars       = dict()
        with open(path,'r') as f:
            for line in f:
                getattr(self, "_"+self.state)(line.strip())

    def _start(self,line):
        if line == "":
            self.state = "files"
        else:
            k,v = line.split("=",2)
            if k not in self.vars:
                self.vars[k] = []
            self.vars[k].append(v)

    def _files(self,line):
        if line == "---":
            self.state = "signatures"
        else:
            self.entries.append(line.split(" "))

    def _signatures(self,line):
        self.signatures.append(line)


mf = Manifest(sys.argv[1])

print mf.vars
print mf.entries
print mf.signatures
