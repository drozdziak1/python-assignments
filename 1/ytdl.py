#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Stanisław Drozd <drozdziak1@gmail.com>

import argparse
import urllib3, certifi
import re
import os, sys

from pytube import YouTube

parser = argparse.ArgumentParser(description="Download a YouTube playlist")

parser.add_argument("--url", metavar="url",
        dest="listURL",
        type=str,
        help="The playlist's URL",
        default="https://www.youtube.com/watch?v=k6U-i4gXkLM&list=PL57FCE46F714A03BC"
        )

parser.add_argument("-C", metavar="dir",
        dest="DLDir",
        type=str,
        help="Destination directory (has to exist)",
        default="./"
        )

args = parser.parse_args()

listURL = args.listURL
DLDir = args.DLDir

if not os.path.exists(DLDir):
    sys.stderr.write("%s: No such file or directory" % DLDir)
    exit(2) # ENOENT

http = urllib3.PoolManager(
        cert_reqs = "CERT_REQUIRED",
        ca_certs = certifi.where() # Fix SSL mistrust warnings
        )

request = http.request("GET", listURL)

if request.status != 200:
    sys.stderr.write("Request failed with status No. %d" % request.status)
    exit(1)

# Match CSS classes of playlist items
pattern = re.compile(r'<a href="(.+?)&.+?"\s*class="\s*spf-link\s*playlist-video\s*clearfix\s*yt-uix-sessionlink\s*spf-link\s*".+?>')

vIDs = pattern.findall(request.data.decode())

i = 1
count = len(vIDs)

for vID in vIDs:
    vURL = "https://youtube.com" + vID

    yt = YouTube(vURL)
    DLFile = DLDir + yt.filename
    print("[%d/%d] Found \"%s\"" % (i, count, yt.filename))

    dupCheck = DLFile + ".mp4"
    nDup = 0

    # Dodge duplicates with a suffix
    while(os.path.exists(dupCheck)):
        nDup += 1
        dupCheck = "%s(%d).mp4" % (DLFile, nDup)

    yt.set_filename(dupCheck)

    # Select the best quality
    yt.filter('mp4')[-1]

    if nDup:
        print("Original name taken, saving to \"%s\"" % dupCheck)
    else:
        print("Saving to \"%s\"" % dupCheck)

    print("Downloading...\n")

    video = yt.get('mp4')
    video.download(dupCheck)


    i += 1
