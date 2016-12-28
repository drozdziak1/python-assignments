#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Stanisław Drozd <drozdziak1@gmail.com>

import argparse
import os
import re

parser = argparse.ArgumentParser(description="Rename TV show related files")
parser.add_argument("--dir", default=".")
args = parser.parse_args()

episodes = os.listdir(args.dir)

pattern = re.compile(r".*[sS](\d+)[eE]0*(\d+).*\.(\w+)$")

i = 0
for episode in episodes:

    match = pattern.match(episode)

    if match:

        nEp = match.group(2)
        extension = match.group(3)

        oldpath = args.dir + "/" + episode
        newpath = args.dir + "/odcinek" + nEp + "." + extension

        print("Renaming %s to %s" % (oldpath, newpath))
        os.rename(oldpath, newpath)
        i += 1

print("Renamed %d episodes" % i)
