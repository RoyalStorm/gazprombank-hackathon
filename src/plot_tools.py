import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


def plot_current_atm(atm_json, axes):
    axes.scatter(
        *np.array([
            np.float64([*obj['geolocation'].values()])[::-1]
            for obj in atm_json
        ]).T,
        marker="2",
        s=250,
        c='red',
        label='Current ATM position',
    )


def plot_new_atm(atm_lon_lat_2d_array, axes):
    axes.scatter(
        *atm_lon_lat_2d_array.T,
        marker="*",
        s=250,
        c='black',
        label='New ATM position',
    )


def plot_clusters_and_atm(atm_json, c, high_traffic_vertex_array, atm_lon_lat_2d_array):
    fig = plt.figure()
    ax = fig.add_subplot(111)

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
        c=cluster_member_colors,
        alpha=0.3
    )

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


def plot_full_map(full_distance_matrix, full_vertex_list, full_vertex_traffic, atm_json, atm_lon_lat_2d_array):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # PLOT EDGES WITH TRAFFIC
    bt = full_vertex_traffic.std() * 1.5
    for i in range(len(full_distance_matrix)):
        for j in range(i, len(full_distance_matrix)):
            if full_distance_matrix[i][j]:
                x1, y1 = full_vertex_list[i]
                x2, y2 = full_vertex_list[j]
                if full_distance_matrix[i][j]['traffic'] > bt:
                    ax.plot([x1, x2], [y1, y2], color='red', linewidth=3.0)
                else:
                    ax.plot([x1, x2], [y1, y2], color='green')

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
