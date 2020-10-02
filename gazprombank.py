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
    # x1y1 = *zip(df['lon1'], df['lat1']),
    # x2y2 = *zip(df['lon2'], df['lat2']),

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

# merged = np.array(list(set(x1y1 + x2y2)))
# c = cluster(merged)
# color_palette = sns.color_palette('Paired', 12)
# cluster_colors = [color_palette[x] if x >= 0
#                   else (0.5, 0.5, 0.5)
#                   for x in c.labels_]
# cluster_member_colors = [sns.desaturate(x, p) for x, p in
#                          zip(cluster_colors, c.probabilities_)]
# plt.scatter(*merged.T, s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)
# plt.show()

vertex_list = [*{*zip(df['lon1'], df['lat1']), *zip(df['lon2'], df['lat2'])}]  # df[['lon1','lat1']].values
vertex_dict = {j: i for i, j in enumerate(vertex_list)}
vertex_number = len(vertex_list)

distance_matrix = [[None] * vertex_number for _ in range(vertex_number)]

for [traffic, x1, y1, x2, y2] in df[['DailyPeoples', 'lon1', 'lat1', 'lon2', 'lat2']].values:
    i, j = vertex_dict[(x1, y1)], vertex_dict[(x2, y2)]
    distance_matrix[i][j] = distance_matrix[j][i] = {'traffic': traffic, 'distance': np.hypot([x2 - x1], [y2 - y1])}

clustering_data = np.array([[np.array([i['traffic'] for i in r if i]).mean()] for r in distance_matrix])

c = cluster(clustering_data)
color_palette = sns.color_palette('Paired', 12)
cluster_colors = [color_palette[x] if x >= 0
                  else (0.5, 0.5, 0.5)
                  for x in c.labels_]
cluster_member_colors = [sns.desaturate(x, p) for x, p in
                         zip(cluster_colors, c.probabilities_)]
plt.scatter(*np.array(vertex_list).T, s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)
plt.show()
