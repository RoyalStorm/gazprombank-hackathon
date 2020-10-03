import json
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from cluster_tools import cluster
from atm_geolocation import get_atm_addresses_by_coords

with open("atm.json") as json_file:
    json_data = json.load(json_file)
    df = pd.read_csv('./savelovsky.csv', sep=';')

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
sns.set(style="ticks", context="talk")
plt.style.use("dark_background")

color_palette = sns.color_palette('bright', 12)
cluster_colors = [color_palette[x] if x >= 0
                  else (0.5, 0.5, 0.5)
                  for x in c.labels_]
cluster_member_colors = [sns.desaturate(x, p) for x, p in
                         zip(cluster_colors, c.probabilities_)]
plt.scatter(*high_traffic_vertex_array.T, s=50, linewidth=0, c=cluster_member_colors)

# PLOT ATM POINTS
clusters_vertex_coords_dict = {
    i: high_traffic_vertex_array[c.labels_ == i]
    for i in np.unique(c.labels_)[1:]
}
atm_lon_lat_2d_array = np.array([v.mean(axis=0) for v in clusters_vertex_coords_dict.values()])

for address in get_atm_addresses_by_coords(np.flip(atm_lon_lat_2d_array, axis=1)):
    print(address)

plt.scatter(*atm_lon_lat_2d_array.T, marker="*", s=250, c='white')

plt.show()
