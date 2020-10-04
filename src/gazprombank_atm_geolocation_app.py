import json
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.atm_geolocation import get_atm_addresses_by_coords
from src.cluster_tools import cluster
from src.plot_tools import plot_full_map, plot_clusters_and_atm


def print_new_atm_addresses(lat_lon_2d_array):
    for address in get_atm_addresses_by_coords(lat_lon_2d_array):
        print(address)


if __name__ == '__main__':
    with open('src/atm_data/savelovsky_atm.json', encoding='utf-8') as json_file:
        atm_json = json.load(json_file)

    traffic_df = pd.read_csv('src/traffic_data/savelovsky_traffic.csv', sep=';')

    full_vertex_list = [*{*zip(traffic_df['lon1'], traffic_df['lat1']),
                          *zip(traffic_df['lon2'], traffic_df['lat2'])}]  # df[['lon1','lat1']].values
    # full_vertex_list = [*{*np.vstack((df[['lon1', 'lat1']].values, df[['lon2', 'lat2']].values))}]
    full_vertex_dict = {j: i for i, j in enumerate(full_vertex_list)}
    full_vertex_number = len(full_vertex_list)

    full_distance_matrix = [
        [None] * full_vertex_number for _ in range(full_vertex_number)
    ]

    for \
            [traffic, x1, y1, x2, y2] in \
            traffic_df[['DailyPeoples', 'lon1', 'lat1', 'lon2', 'lat2']].values:
        i, j = full_vertex_dict[(x1, y1)], full_vertex_dict[(x2, y2)]
        full_distance_matrix[i][j] = full_distance_matrix[j][i] = {
            'traffic': traffic,
            'distance': math.hypot(x2 - x1, y2 - y1)
        }

    full_vertex_traffic = np.array([
        [np.array([i['traffic'] for i in r if i]).mean()]
        for r in full_distance_matrix
    ])

    high_traffic_vertex_df_index = [
        v for v, t in zip(range(full_vertex_number), full_vertex_traffic)  # enumerate???
        if t > (vt_mean := full_vertex_traffic.std() * 1.5)
    ]
    high_traffic_vertex_array = \
        np.array(full_vertex_list)[high_traffic_vertex_df_index]
    high_traffic_vertex_number = len(high_traffic_vertex_df_index)

    high_traffic_vertex_df = pd.DataFrame(
        [
            [full_distance_matrix[i][j] for j in high_traffic_vertex_df_index]
            for i in high_traffic_vertex_df_index
        ],
        index=high_traffic_vertex_df_index,
        columns=high_traffic_vertex_df_index
    )

    c = cluster(high_traffic_vertex_array)

    # SET PLOT THEME
    # sns.set(style='ticks', context='talk')
    # plt.style.use('dark_background')

    # GET ATM COORDS
    atm_lon_lat_2d_array = np.array([
        high_traffic_vertex_array[c.labels_ == i].mean(axis=0)
        for i in np.unique(c.labels_)[1:]
    ])

    print_new_atm_addresses(np.flip(atm_lon_lat_2d_array, axis=1))

    # SHOW PLOTS
    plot_clusters_and_atm(atm_json, c, high_traffic_vertex_array, atm_lon_lat_2d_array)
    plot_full_map(full_distance_matrix, full_vertex_list, full_vertex_traffic, atm_json, atm_lon_lat_2d_array)

    plt.show()
