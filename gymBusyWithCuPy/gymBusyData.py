# dogOrCatData.py — loads real images into sampleIns and sampleOuts, and saves resized versions

from PIL import Image
import os
import cupy as cp

SAMPLE_SIZE = 300

#chatgpt generated gym time data
'''
🧠 Input Features (in order in input array):
hour (0–11) → morning/evening 12-hour format

am_pm (0 = AM, 1 = PM)

day_of_week (0 = Monday, ..., 6 = Sunday)

🧮 Output:
Single float [0.0 – 1.0] = estimated % of machines in use
'''

data = [([3, 1, 3], [0.27]),
 ([2, 1, 4], [0.31]),
 ([9, 0, 2], [0.19]),
 ([1, 0, 6], [0.16]),
 ([10, 0, 6], [0.35]),
 ([3, 0, 0], [0.22]),
 ([4, 1, 3], [0.84]),
 ([0, 0, 4], [0.22]),
 ([5, 1, 6], [0.21]),
 ([7, 1, 5], [0.19]),
 ([2, 0, 2], [0.25]),
 ([7, 0, 6], [0.21]),
 ([1, 0, 5], [0.18]),
 ([4, 0, 3], [0.16]),
 ([4, 1, 4], [0.67]),
 ([4, 0, 6], [0.23]),
 ([9, 0, 2], [0.23]),
 ([11, 0, 5], [0.41]),
 ([1, 0, 6], [0.21]),
 ([10, 1, 0], [0.21]),
 ([2, 0, 2], [0.22]),
 ([2, 1, 6], [0.32]),
 ([6, 0, 1], [0.3]),
 ([0, 1, 5], [0.35]),
 ([10, 1, 1], [0.16]),
 ([7, 1, 5], [0.16]),
 ([9, 1, 6], [0.23]),
 ([11, 1, 5], [0.2]),
 ([0, 1, 3], [0.33]),
 ([2, 0, 3], [0.15]),
 ([4, 0, 4], [0.17]),
 ([5, 0, 1], [0.25]),
 ([10, 0, 1], [0.2]),
 ([9, 0, 2], [0.19]),
 ([2, 0, 3], [0.16]),
 ([0, 0, 2], [0.22]),
 ([8, 1, 3], [0.82]),
 ([4, 0, 4], [0.16]),
 ([11, 1, 4], [0.19]),
 ([2, 1, 4], [0.32]),
 ([5, 1, 6], [0.18]),
 ([9, 0, 1], [0.17]),
 ([1, 1, 1], [0.31]),
 ([6, 1, 0], [0.81]),
 ([10, 0, 0], [0.18]),
 ([11, 0, 1], [0.16]),
 ([4, 0, 6], [0.23]),
 ([11, 0, 4], [0.21]),
 ([3, 1, 2], [0.29]),
 ([9, 0, 6], [0.4]),
 ([9, 0, 1], [0.19]),
 ([5, 0, 5], [0.15]),
 ([7, 1, 1], [0.66]),
 ([0, 1, 6], [0.26]),
 ([6, 1, 4], [0.79]),
 ([2, 1, 3], [0.3]),
 ([8, 0, 4], [0.37]),
 ([2, 0, 6], [0.19]),
 ([2, 1, 6], [0.31]),
 ([0, 1, 6], [0.34]),
 ([5, 1, 6], [0.16]),
 ([10, 0, 3], [0.22]),
 ([4, 1, 1], [0.79]),
 ([7, 1, 5], [0.24]),
 ([11, 0, 4], [0.22]),
 ([9, 1, 3], [0.22]),
 ([6, 1, 1], [0.67]),
 ([9, 1, 5], [0.21]),
 ([0, 0, 0], [0.16]),
 ([3, 1, 5], [0.28]),
 ([4, 1, 4], [0.68]),
 ([9, 1, 2], [0.17]),
 ([0, 0, 0], [0.17]),
 ([0, 0, 2], [0.22]),
 ([10, 1, 4], [0.17]),
 ([8, 1, 4], [0.8]),
 ([11, 1, 2], [0.22]),
 ([8, 0, 2], [0.48]),
 ([11, 1, 2], [0.21]),
 ([5, 0, 6], [0.22]),
 ([5, 0, 3], [0.21]),
 ([0, 1, 0], [0.35]),
 ([11, 1, 3], [0.18]),
 ([6, 1, 1], [0.67]),
 ([3, 0, 3], [0.21]),
 ([6, 0, 5], [0.17]),
 ([11, 0, 5], [0.41]),
 ([3, 1, 3], [0.3]),
 ([6, 0, 4], [0.39]),
 ([3, 0, 4], [0.17]),
 ([8, 0, 5], [0.19]),
 ([11, 1, 2], [0.24]),
 ([6, 0, 6], [0.18]),
 ([11, 1, 5], [0.18]),
 ([6, 0, 0], [0.41]),
 ([3, 1, 5], [0.3]),
 ([1, 1, 4], [0.28]),
 ([1, 1, 2], [0.34]),
 ([4, 1, 5], [0.24]),
 ([5, 1, 0], [0.79]),
 ([5, 1, 5], [0.24]),
 ([9, 1, 0], [0.22]),
 ([4, 0, 5], [0.15]),
 ([3, 0, 2], [0.21]),
 ([2, 0, 5], [0.18]),
 ([1, 1, 6], [0.35]),
 ([9, 0, 0], [0.17]),
 ([9, 0, 4], [0.25]),
 ([7, 0, 6], [0.18]),
 ([8, 1, 0], [0.68]),
 ([5, 0, 6], [0.23]),
 ([7, 1, 5], [0.15]),
 ([6, 0, 5], [0.19]),
 ([10, 0, 0], [0.18]),
 ([9, 1, 5], [0.21]),
 ([11, 0, 2], [0.15]),
 ([10, 0, 3], [0.2]),
 ([5, 0, 0], [0.16]),
 ([11, 0, 4], [0.17]),
 ([0, 0, 2], [0.18]),
 ([7, 1, 2], [0.71]),
 ([0, 1, 5], [0.28]),
 ([11, 1, 2], [0.16]),
 ([11, 0, 2], [0.23]),
 ([11, 1, 6], [0.23]),
 ([8, 0, 5], [0.24]),
 ([9, 1, 2], [0.21]),
 ([2, 1, 5], [0.3]),
 ([10, 1, 3], [0.15]),
 ([2, 1, 1], [0.31]),
 ([1, 0, 3], [0.17]),
 ([4, 0, 0], [0.21]),
 ([3, 0, 3], [0.24]),
 ([2, 0, 6], [0.15]),
 ([6, 1, 3], [0.74]),
 ([8, 1, 6], [0.17]),
 ([1, 1, 6], [0.32]),
 ([11, 0, 5], [0.39]),
 ([3, 1, 2], [0.28]),
 ([2, 0, 6], [0.19]),
 ([1, 0, 1], [0.22]),
 ([1, 1, 1], [0.33]),
 ([1, 0, 2], [0.22]),
 ([4, 0, 4], [0.24]),
 ([11, 0, 4], [0.21]),
 ([7, 0, 0], [0.34]),
 ([6, 0, 0], [0.4]),
 ([5, 1, 6], [0.24]),
 ([1, 1, 5], [0.29]),
 ([11, 1, 0], [0.19]),
 ([4, 1, 4], [0.77]),
 ([11, 0, 4], [0.19]),
 ([6, 1, 1], [0.7]),
 ([6, 0, 4], [0.35]),
 ([4, 1, 5], [0.23]),
 ([10, 0, 3], [0.22]),
 ([3, 0, 2], [0.18]),
 ([11, 1, 1], [0.2]),
 ([8, 0, 5], [0.16]),
 ([6, 1, 5], [0.15]),
 ([5, 0, 1], [0.17]),
 ([0, 0, 0], [0.24]),
 ([8, 1, 4], [0.8]),
 ([8, 1, 2], [0.79]),
 ([1, 0, 6], [0.23]),
 ([6, 0, 5], [0.17]),
 ([8, 1, 6], [0.18]),
 ([3, 1, 6], [0.3]),
 ([10, 0, 6], [0.46]),
 ([5, 1, 5], [0.21]),
 ([4, 0, 2], [0.24]),
 ([3, 1, 5], [0.28]),
 ([0, 0, 3], [0.24]),
 ([7, 1, 1], [0.78]),
 ([10, 0, 2], [0.23]),
 ([4, 0, 1], [0.17]),
 ([11, 0, 4], [0.22]),
 ([11, 0, 6], [0.43]),
 ([3, 0, 4], [0.2]),
 ([0, 0, 6], [0.19]),
 ([1, 0, 2], [0.16]),
 ([4, 1, 2], [0.72]),
 ([8, 1, 1], [0.67]),
 ([11, 0, 6], [0.48]),
 ([2, 1, 1], [0.28]),
 ([3, 0, 1], [0.19]),
 ([7, 0, 0], [0.33]),
 ([0, 0, 0], [0.23]),
 ([11, 1, 6], [0.18]),
 ([7, 0, 5], [0.19]),
 ([10, 0, 4], [0.21]),
 ([0, 1, 6], [0.27]),
 ([1, 1, 4], [0.29]),
 ([9, 0, 5], [0.49]),
 ([0, 1, 6], [0.29]),
 ([3, 0, 0], [0.24]),
 ([5, 0, 2], [0.23]),
 ([9, 0, 5], [0.46]),
 ([1, 1, 1], [0.34]),
 ([11, 1, 6], [0.2]),
 ([7, 0, 1], [0.33]),
 ([2, 1, 1], [0.31]),
 ([6, 1, 5], [0.17]),
 ([2, 1, 3], [0.34]),
 ([0, 1, 6], [0.35]),
 ([6, 0, 6], [0.23]),
 ([6, 1, 0], [0.79]),
 ([10, 1, 0], [0.21]),
 ([8, 1, 0], [0.71]),
 ([4, 1, 5], [0.2]),
 ([0, 0, 0], [0.19]),
 ([6, 0, 2], [0.44]),
 ([8, 0, 6], [0.21]),
 ([5, 1, 6], [0.17]),
 ([9, 1, 3], [0.17]),
 ([8, 1, 2], [0.74]),
 ([0, 1, 3], [0.25]),
 ([3, 1, 3], [0.33]),
 ([9, 1, 3], [0.15]),
 ([3, 0, 0], [0.16]),
 ([6, 0, 6], [0.21]),
 ([4, 1, 6], [0.21]),
 ([6, 0, 5], [0.22]),
 ([4, 1, 2], [0.83]),
 ([4, 1, 4], [0.84]),
 ([2, 0, 6], [0.21]),
 ([10, 1, 5], [0.19]),
 ([11, 0, 0], [0.24]),
 ([11, 1, 1], [0.2]),
 ([9, 0, 5], [0.47]),
 ([9, 0, 1], [0.17]),
 ([4, 0, 6], [0.21]),
 ([4, 0, 1], [0.17]),
 ([3, 1, 6], [0.3]),
 ([9, 1, 0], [0.21]),
 ([8, 1, 4], [0.78]),
 ([10, 1, 1], [0.19]),
 ([5, 0, 5], [0.23]),
 ([6, 1, 5], [0.21]),
 ([11, 0, 6], [0.39]),
 ([7, 1, 1], [0.69]),
 ([10, 1, 4], [0.19]),
 ([2, 0, 4], [0.18]),
 ([0, 1, 5], [0.32]),
 ([3, 1, 1], [0.32]),
 ([0, 0, 6], [0.18]),
 ([2, 0, 6], [0.15]),
 ([1, 0, 1], [0.2]),
 ([6, 1, 6], [0.16]),
 ([11, 0, 5], [0.39]),
 ([6, 0, 0], [0.44]),
 ([10, 1, 2], [0.21]),
 ([9, 1, 3], [0.15]),
 ([8, 1, 5], [0.24]),
 ([5, 1, 0], [0.67]),
 ([4, 0, 3], [0.17]),
 ([7, 1, 4], [0.84]),
 ([6, 1, 2], [0.73]),
 ([9, 0, 5], [0.44]),
 ([7, 0, 1], [0.46]),
 ([2, 1, 4], [0.27]),
 ([7, 1, 4], [0.84]),
 ([9, 1, 0], [0.24]),
 ([4, 0, 4], [0.19]),
 ([1, 1, 3], [0.27]),
 ([7, 0, 6], [0.17]),
 ([5, 0, 1], [0.21]),
 ([6, 0, 0], [0.33]),
 ([10, 0, 0], [0.16]),
 ([8, 0, 3], [0.49]),
 ([8, 0, 6], [0.2]),
 ([1, 1, 1], [0.31]),
 ([2, 0, 4], [0.23]),
 ([9, 0, 6], [0.36]),
 ([2, 1, 4], [0.26]),
 ([1, 1, 5], [0.27]),
 ([2, 0, 0], [0.17]),
 ([6, 0, 6], [0.22]),
 ([2, 1, 5], [0.33]),
 ([2, 0, 0], [0.21]),
 ([2, 0, 5], [0.18]),
 ([3, 1, 0], [0.27]),
 ([6, 0, 4], [0.4]),
 ([2, 0, 2], [0.21]),
 ([3, 0, 6], [0.17]),
 ([1, 1, 6], [0.31]),
 ([9, 0, 1], [0.21]),
 ([5, 0, 0], [0.2]),
 ([10, 0, 3], [0.24]),
 ([0, 1, 5], [0.32]),
 ([10, 0, 5], [0.49]),
 ([2, 1, 2], [0.34]),
 ([9, 1, 0], [0.16]),
 ([7, 0, 0], [0.44]),
 ([1, 1, 5], [0.32]),
 ([0, 1, 1], [0.32]),
 ([6, 0, 5], [0.19]),
 ([0, 1, 1], [0.32]),
 ([7, 0, 0], [0.47]),
 ([0, 0, 6], [0.16])]

#   adding my own data to account for AM hours
for day in range(7):
    for hour in range(1, 5):
        data.append(([hour, 0, day], [0.0]))

# Split into separate arrays
sampleIns = [cp.array(inp, dtype=cp.float32) for inp, _ in data]
sampleOuts = [cp.array(out, dtype=cp.float32) for _, out in data]