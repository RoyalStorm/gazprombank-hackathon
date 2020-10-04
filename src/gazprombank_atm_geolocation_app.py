import json
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.cluster_tools import cluster
from src.atm_geolocation import get_atm_addresses_by_coords


# todo
# график с картой и банкоматами, цвет ребер меняется плавно вместе с трафиком

def plot_current_atm(atm_json, axes):
    axes.scatter(
        *np.array([
            np.float64([*obj['geolocation'].values()])[::-1]
            for obj in atm_json
        ]).T,
        marker="2",
        s=250,
        c='red',
        label='Current ATM position'
    )


def plot_new_atm(atm_lon_lat_2d_array, axes):
    axes.scatter(
        *atm_lon_lat_2d_array.T,
        marker="*",
        s=250,
        c='black',
        label='New ATM position'
    )


def plot_clusters_and_atm(atm_json, c, high_traffic_vertex_array, atm_lon_lat_2d_array):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # PLOT CURRENT ATM
    plot_current_atm(atm_json, ax)

    # PLOT HIGH TRAFFIC VERTICES
    color_palette = sns.color_palette('bright', 12)
    cluster_colors = [color_palette[x] if x >= 0
                      else (0.5, 0.5, 0.5)
                      for x in c.labels_]
    cluster_member_colors = [sns.desaturate(x, p) for x, p in
                             zip(cluster_colors, c.probabilities_)]
    ax.scatter(
        *high_traffic_vertex_array.T,
        s=50,
        linewidth=0,
        c=cluster_member_colors
    )

    # PLOT NEW ATM POINTS
    plot_new_atm(atm_lon_lat_2d_array, ax)
    # ax.scatter(
    #     *atm_lon_lat_2d_array.T,
    #     marker="*",
    #     s=250,
    #     c='black',
    #     label='New ATM position'
    # )

    ax.legend(
        fontsize=8,
        facecolor='oldlace',
        edgecolor='r',
        loc='lower right'
    )

    # fig.show()

    # x1x2 = *zip(traffic_df['lon1'], traffic_df['lon2']),
    # y1y2 = *zip(traffic_df['lat1'], traffic_df['lat2']),
    #
    # points = []
    # for i in range(0, len(atm_json)):
    #     p = atm_json[i]['geolocation'].values()
    #     y, x = map(float, p)
    #     points.append((x, y))
    # for obj in atm_json:
    #     lat, lon = np.float64(obj['geolocation'].values())
    #     np.array([obj['geolocation']['longitude']])
    #     points.append((lon, lat))


def plot_full_map(traffic_df, atm_json, atm_lon_lat_2d_array):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # PLOT CURRENT ATM
    plot_current_atm(atm_json, ax)

    # PLOT NEW ATM POINTS
    plot_new_atm(atm_lon_lat_2d_array, ax)

    ax.legend(
        fontsize=8,
        facecolor='oldlace',
        edgecolor='r',
        loc='lower right'
    )


def print_new_atm_addresses(lat_lon_2d_array):
    for address in get_atm_addresses_by_coords(lat_lon_2d_array):
        print(address)


if __name__ == '__main__':
    with open('src/atm_data/south_medvedkovo_atm.json', encoding='utf-8') as json_file:
        atm_json = json.load(json_file)

    traffic_df = pd.read_csv('src/traffic_data/south_medvedkovo_traffic.csv', sep=';')

    # PLOT EDGES
    # for ind, (i, j) in enumerate(zip(x1x2, y1y2)):
    #     plt.plot(i, j, color)

    # plt.xscale('log')
    # plt.yscale('log')
    # plt.show()

    ##########

    full_vertex_list = [*{*zip(traffic_df['lon1'], traffic_df['lat1']),
                          *zip(traffic_df['lon2'], traffic_df['lat2'])}]  # df[['lon1','lat1']].values
    # full_vertex_list = [*{*np.vstack((df[['lon1', 'lat1']].values, df[['lon2', 'lat2']].values))}]
    full_vertex_dict = {j: i for i, j in enumerate(full_vertex_list)}
    full_vertex_number = len(full_vertex_list)

    full_edge_matrix = [
        [None] * full_vertex_number for _ in range(full_vertex_number)
    ]

    for \
            [traffic, x1, y1, x2, y2] in \
            traffic_df[['DailyPeoples', 'lon1', 'lat1', 'lon2', 'lat2']].values:
        i, j = full_vertex_dict[(x1, y1)], full_vertex_dict[(x2, y2)]
        full_edge_matrix[i][j] = full_edge_matrix[j][i] = {
            'traffic': traffic,
            'distance': math.hypot(x2 - x1, y2 - y1)
        }

    full_vertex_traffic = np.array([  # ????????????????
        [np.array([i['traffic'] for i in r if i]).mean()]
        for r in full_edge_matrix  # ??????????????????????????
    ])

    high_traffic_vertex_df_index = [
        v for v, t in zip(range(full_vertex_number), full_vertex_traffic)
        if t > (vt_mean := full_vertex_traffic.std() * 1.5)
    ]
    high_traffic_vertex_array = \
        np.array(full_vertex_list)[high_traffic_vertex_df_index]
    high_traffic_vertex_number = len(high_traffic_vertex_df_index)

    high_traffic_vertex_df = pd.DataFrame(
        [
            [full_edge_matrix[i][j] for j in high_traffic_vertex_df_index]  # ?????????????????/
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

    ###all plots here### pca pfm

    plot_clusters_and_atm(atm_json, c, high_traffic_vertex_array, atm_lon_lat_2d_array)
    plot_full_map(atm_json, atm_lon_lat_2d_array)

    plt.show()

    # PLOT CURRENT ATM pca pfm
    # x1x2 = *zip(df['lon1'], df['lon2']),
    # y1y2 = *zip(df['lat1'], df['lat2']),
    #
    # points = []
    # for i in range(0, len(json_data)):
    #     p = json_data[i]['geolocation'].values()
    #     y, x = map(float, p)
    #     points.append((x, y))
    #
    # # plt.plot(*zip(*points), 'bo', label='Current ATM position')
    # plt.scatter(*zip(*points), marker="2", s=250, c='red', label='Current ATM position')

    # PLOT HIGH TRAFFIC VERTICES pca
    # color_palette = sns.color_palette('bright', 12)
    # cluster_colors = [color_palette[x] if x >= 0
    #                   else (0.5, 0.5, 0.5)
    #                   for x in c.labels_]
    # cluster_member_colors = [sns.desaturate(x, p) for x, p in
    #                          zip(cluster_colors, c.probabilities_)]
    # plt.scatter(
    #     *high_traffic_vertex_array.T,
    #     s=50,
    #     linewidth=0,
    #     c=cluster_member_colors
    # )

    # PLOT NEW ATM POINTS pca pfm
    # plt.scatter(*atm_lon_lat_2d_array.T, marker="*", s=250, c='black', label='New ATM position')
    #
    # plt.legend(
    #     fontsize=8,
    #     facecolor='oldlace',
    #     edgecolor='r',
    #     loc='lower right'
    # )
    #
    # plt.show()
