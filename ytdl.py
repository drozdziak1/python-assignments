#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import certifi, urllib3, re, os

from pytube import YouTube

# Download location (has to exist), filename conflicts not resolved yet
DLDir = "./"

# Default list URL
listURL = "https://www.youtube.com/watch?v=k6U-i4gXkLM&list=PL57FCE46F714A03BC"

http = urllib3.PoolManager(
        cert_reqs = "CERT_REQUIRED",
        ca_certs = certifi.where() # Fix SSL mistrust warnings
        )

request = http.request("GET", listURL)

# match CSS classes of playlist items
pattern = re.compile(r'<a href="(.+?)&.+?"\s*class="\s*spf-link\s*playlist-video\s*clearfix\s*yt-uix-sessionlink\s*spf-link\s*".+?>')

if request.status != 200:
    print("Request returned error No. %d" % request.status)
    exit(1)

if not os.path.exists(DLDir):
    os.mkdir(DLDir)

vIDs = pattern.findall(request.data.decode())

i = 1
count = len(vIDs)

for vID in vIDs:
    vURL = "https://youtube.com" + vID
    print("[%d/%d] Found " % (i, count) + vURL)
    print("Downloading...")

    yt = YouTube(vURL)
    DLFile = DLDir + yt.filename

    dupCheck = DLFile + ".mp4"
    copy_n = 1

    # Add an incrementing suffix if the file exists
    while(os.path.exists(dupCheck)):
        dupCheck = DLFile + "(%d)" % copy_n + ".mp4"
        copy_n += 1

    yt.set_filename(dupCheck)

    yt.filter('mp4')[-1] # Select the best quality
    video = yt.get('mp4')

    video.download(dupCheck)
    print(dupCheck + " done.")
    i += 1
