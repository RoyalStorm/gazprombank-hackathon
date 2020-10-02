import json

import matplotlib.pyplot as plt
import pandas as pd

with open("out.json") as json_file:
    json_data = json.load(json_file)
    df = pd.read_csv('./sav.csv', sep=';')
    x1x2 = *zip(df['lon1'], df['lon2']),
    y1y2 = *zip(df['lat1'], df['lat2']),

points = []
for i in range(0, len(json_data)):
    p = json_data[i]['geolocation'].values()
    y, x = map(float, p)
    points.append((x, y))

plt.xscale('log')
plt.yscale('log')
plt.plot(*zip(*points), 'ro')

key = 'DailyPeoples'
for ind, (i, j) in enumerate(zip(x1x2, y1y2)):
    color = None
    if df[key][ind] > 3000:
        color = 'r'
    else:
        color = 'g'
    plt.plot(i, j, color)
plt.show()

print(min(df[key]), max(df[key]))
