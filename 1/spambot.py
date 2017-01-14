#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Stanisław Drozd <drozdziak1@gmail.com>

import argparse
import urllib3, certifi
import re
import sys # Rid "|" users of garbage in stdout

parser = argparse.ArgumentParser(
        description="Extract e-mail addresses from a website.")

parser.add_argument(
        "-u",
        metavar="url",
        type=str,
        help="crawl through url specifically",
        default="http://vps276855.ovh.net/", # A test setup on my private VPS
        dest="url",
        )

parser.add_argument(
        "-o",
        metavar="output_file",
        type=str,
        help="save to output_file (stdout by default)",
        dest="output_file",
        )


args = parser.parse_args()

if args.output_file:
    fout = open(args.output_file, "w");
else:
    fout = sys.stdout

http = urllib3.PoolManager(
        cert_reqs = "CERT_REQUIRED",
        ca_certs = certifi.where() # Fix SSL mistrust warnings
        )

try:
    request = http.request("GET", args.url)
except urllib3.exceptions.MaxRetryError:
    sys.stderr.write("HTTP request failed.\n")
    exit(1)

if request.status != 200:
    sys.stderr.write("HTTP request failed with status No. %d\n" % request.status)
    exit(1)

# Should have probably used the email module
searchPattern = re.compile(r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")

# Note: Ignoring encoding errors WRT utf-8
emails = searchPattern.findall(request.data.decode(errors="ignore"))

count = len(emails)

if(count >= 2):
    sys.stderr.write("Found %d addresses.\n" % count)
elif(count):
    sys.stderr.write("Found 1 address.\n")
else:
    sys.stderr.write("No e-mail addresses found.\n")
    exit(1) # Following grep's "no matches -> non-zero exit" convention

sys.stderr.flush()

for email in emails:
    fout.write("%s...%s@%s\n"% (email[0][0], email[0][-1], email[1]))

if args.output_file:
    fout.close()
