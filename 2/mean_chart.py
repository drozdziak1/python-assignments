#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Stanisław Drozd <drozdziak1@gmail.com>

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_csv("chart_data.csv")

# Prevent scientific notation of chart's graduation
mpl.rcParams["axes.formatter.useoffset"] = False

# Fix misrendered unicode characters
mpl.rc('font', family='Arial')

# Set axes ranges
plt.axis([
    df.year.min() - 1, df.year.max() + 1,
    df.grade.min() - 1, df.grade.max() + 1])

plt.xlabel("Rok")
plt.ylabel("Oceny")

for year, records in df.groupby(df.year):
    plt.plot(records.year, records.grade, "wo")
    plt.plot(year, records.grade.median(), "rv")
    plt.plot(year, records.grade.mean(), "g^")

plt.show()
