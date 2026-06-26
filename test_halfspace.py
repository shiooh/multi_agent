from depth.model.DepthEucl import DepthEucl
import numpy as np
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

d = 2
N = 10

points = np.array([[random.uniform(0, 50) for _ in range(d)] for i in range(N)])
model=DepthEucl().load_dataset(points)

depths = model.halfspace(points, exact=True)
# depths = [depth * N for depth in depths]

print(points)
print(depths)

center_idx = depths.argmax()
centerpoint = points[center_idx]

print(centerpoint)

Figure, ax = plt.subplots()
for (point, depth) in zip(points,depths):
    ax.scatter(point[0], point[1],c='b')
    plt.annotate(depth, xy=(point[0], point[1]))

ax.scatter([centerpoint[0]], [centerpoint[1]], c='r')
ax.set_xlim(0, 50)
ax.set_ylim(0, 50)
Figure.savefig('out/centerpoin.png')