#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import urllib3, certifi
import re
from sys import stderr # Rid "|" pipe users of garbage in output

parser = argparse.ArgumentParser(
        description="Extract e-mail addresses from a website.")

parser.add_argument("--url", metavar="url",
        type=str,
        help="crawl through url specifically",
        default="https://www.wmi.amu.edu.pl/pl/pracownicy"
        )

args = parser.parse_args()

http = urllib3.PoolManager(
        cert_reqs = "CERT_REQUIRED",
        ca_certs = certifi.where() # Fix SSL mistrust warnings
        )

try:
    request = http.request("GET", args.url)
except urllib3.exceptions.MaxRetryError:
    stderr.write("HTTP request failed.\n")
    exit(1)

if request.status != 200:
    stderr.write("HTTP request failed with status No. %d\n" % request.status)
    exit(1)

# Should have probably used the email module
searchPattern = re.compile(r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")

# Note: Ignoring encoding errors WRT utf-8
emails = searchPattern.findall(request.data.decode(errors="ignore"))

count = len(emails)

if(count >= 2):
    stderr.write("Found %d Addresses:\n" % count)
elif(count):
    stderr.write("Found 1 Address:\n")
else:
    stderr.write("No e-mail addresses found.\n")
    # grep exits non-zero without matches, following
    # this convention seems reasonable
    exit(1)

stderr.flush()
for email in emails:
    print("%s...%s@%s"% (email[0][0], email[0][-1], email[1]))
