import json
import math
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

full_vertex_list = [*{*zip(df['lon1'], df['lat1']), *zip(df['lon2'], df['lat2'])}]  # df[['lon1','lat1']].values
full_vertex_dict = {j: i for i, j in enumerate(full_vertex_list)}
full_vertex_number = len(full_vertex_list)

full_edge_matrix = [[None] * full_vertex_number for _ in range(full_vertex_number)]

for \
        [traffic, x1, y1, x2, y2] in \
        df[['DailyPeoples', 'lon1', 'lat1', 'lon2', 'lat2']].values:
    i, j = full_vertex_dict[(x1, y1)], full_vertex_dict[(x2, y2)]
    full_edge_matrix[i][j] = full_edge_matrix[j][i] = {
        'traffic': traffic,
        'distance': math.hypot(x2 - x1, y2 - y1)
    }

full_vertex_traffic = np.array([
    [np.array([i['traffic'] for i in r if i]).mean()] for r in full_edge_matrix
])

high_traffic_vertex_df_index = [
    v for v, t in zip(range(full_vertex_number), full_vertex_traffic)
    if t > (vt_mean := full_vertex_traffic.std() * 1.5)
]
high_traffic_vertex_array = np.array(full_vertex_list)[high_traffic_vertex_df_index]  # todo rename
high_traffic_vertex_number = len(high_traffic_vertex_df_index)

high_traffic_vertex_df = pd.DataFrame(
    [
        [full_edge_matrix[i][j] for j in high_traffic_vertex_df_index]
        for i in high_traffic_vertex_df_index
    ],
    index=high_traffic_vertex_df_index,
    columns=high_traffic_vertex_df_index
)

c = cluster(high_traffic_vertex_array)

# PLOT HIGH TRAFFIC VERTICES
color_palette = sns.color_palette('Paired', 12)
cluster_colors = [color_palette[x] if x >= 0
                  else (0.5, 0.5, 0.5)
                  for x in c.labels_]
cluster_member_colors = [sns.desaturate(x, p) for x, p in
                         zip(cluster_colors, c.probabilities_)]
plt.scatter(*high_traffic_vertex_array.T, s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)

# PLOT ATM POINTS
clusters_vertex_coords_dict = {
    i: high_traffic_vertex_array[c.labels_ == i]
    for i in np.unique(c.labels_)
}
atm_point_list = []
for v in clusters_vertex_coords_dict.values():
    minx, maxx, miny, maxy = (100, 0) * 2

    for i in range(len(v)):
        if (v[i, 0] < minx):
            minx = v[i, 0]
        if (v[i, 0] > maxx):
            maxx = v[i, 0]
        if (v[i, 1] < miny):
            miny = v[i, 1]
        if (v[i, 1] > maxy):
            maxy = v[i, 1]
    x0 = (maxx - minx) / 2
    y0 = (maxy - miny) / 2

    atm_point = [v[0, 0], v[0, 1]]

    for i in range(len(v)):
        if (abs(v[i, 0] - x0) < abs(atm_point[0] - x0)) and (abs(v[i, 1] - y0) < abs(atm_point[1] - y0)):
            atm_point[0] = v[i, 0]
            atm_point[1] = v[i, 1]

    atm_point_list.append(atm_point)

for i in atm_point_list:
    plt.scatter(*i, marker="*", s=250, c='orange', alpha=0.9)

plt.show()
exit()

plt.figure()

plt.scatter(
    *high_traffic_vertex_array.T,
    #     s=50,
    #     linewidth=0,
    #     c=cluster_member_colors,
    #     alpha=0.25
)

# for [v1, v2], value in np.ndenumerate(high_traffic_vertex_df.values):
#     if value:
#         plt.plot(  # todo цвет в зависимости от значения value['traffic']
#             *np.array([
#                 full_vertex_list[v1], full_vertex_list[v2],
#             ]).T
#         )  # x1 y1 \n x2 y2

plt.show()
