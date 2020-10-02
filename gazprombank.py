import json

import matplotlib.pyplot as plt
import pandas as pd
from cluster_tools import cluster
import numpy as np
import seaborn as sns

with open("atm.json") as json_file:
    json_data = json.load(json_file)
    df = pd.read_csv('./sav.csv', sep=';')
    # x1x2 = *zip(df['lon1'], df['lon2']),
    # y1y2 = *zip(df['lat1'], df['lat2']),
    x1y1 = *zip(df['lat1'], df['lon1']),
    x2y2 = *zip(df['lat2'], df['lon2']),

"""points = []
for i in range(0, len(json_data)):
    p = json_data[i]['geolocation'].values()
    y, x = map(float, p)
    points.append((x, y))

plt.xscale('log')
plt.yscale('log')
plt.plot(*zip(*points), 'bo')

for ind, (i, j) in enumerate(zip(x1x2, y1y2)):
    color = None
    if df['DailyPeoples'][ind] > 3000:
        color = 'r'
    else:
        color = 'g'
    plt.plot(i, j, color)

plt.show()"""

merged = np.array(list(set(x1y1 + x2y2)))
c = cluster(merged)
color_palette = sns.color_palette('Paired', 12)
cluster_colors = [color_palette[x] if x >= 0
                  else (0.5, 0.5, 0.5)
                  for x in c.labels_]
cluster_member_colors = [sns.desaturate(x, p) for x, p in
                         zip(cluster_colors, c.probabilities_)]
plt.scatter(*merged.T, s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)
plt.show()
