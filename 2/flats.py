#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Stanisław Drozd <drozdziak1@gmail.com>

import pandas

df = pandas.read_csv("http://samplecsvs.s3.amazonaws.com/Sacramentorealestatetransactions.csv")

ad1 = df[df.beds > 4].sort("beds", ascending=0) # desc order for easier checking
ad1 = ad1.reset_index(drop=True)
print("Ad1:\n", ad1[["street", "city", "zip", "state", "beds"]])

ad2 = df["price"].sum()
print("Ad2: $%d" % ad2)

ad3 = df[df.sq__ft < 900].sort("sq__ft", ascending=1)
ad3 = ad3.reset_index(drop=True)
print("Ad3:\n", ad3[["street", "city", "zip", "state", "sq__ft"]])
