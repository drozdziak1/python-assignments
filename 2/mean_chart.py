#!/usr/bin/env python3
# Stanisław Drozd <drozdziak1@gmail.com>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("chart_data.csv")

for year, records in df.groupby(df.year):
    plt.plot(year, records.grade.mean(), "g^")

plt.show()
