#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Stanisław Drozd <drozdziak1@gmail.com>

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


df = pd.read_csv("chart_data.csv")

# Randomize grade values
# df.grade = np.random.choice(np.arange(2, 5, .01), len(df))

# Shuffle records
# df = df.iloc[np.random.permutation(len(df))]

# Prevent scientific graduation notation
mpl.rcParams["axes.formatter.useoffset"] = False

# Fix misrendered unicode characters
mpl.rc("font", family="Arial")

plt.axis([
    df.year.min() - 1, df.year.max() + 1,
    df.grade.min() - 1, df.grade.max() + 1
])

plt.xlabel("Rok")
plt.ylabel("Oceny")

for year, records in df.groupby(df.year):
    grade, = plt.plot(records.year, records.grade, "wo")
    mean, = plt.plot(year, records.grade.mean(), "g^")

plt.legend([grade, mean], ["Oceny", "Średnia"], numpoints=1)
plt.show()
