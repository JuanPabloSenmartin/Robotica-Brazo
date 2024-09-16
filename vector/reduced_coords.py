from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import numpy
import random
import math


def reduced_coords(x_coords, y_coords, factor):
    n_points = int(len(x_coords) * factor)
    x_coords = numpy.array(x_coords)
    x_min = x_coords.min()
    x_max = x_coords.max()
    x_range = x_max - x_min
    distances = []
    tallied_distances = [0]
    tallied_distance = 0
    for i in range(0, len(x_coords) - 1):
        xi = x_coords[i]
        xf = x_coords[i + 1]
        yi = y_coords[i]
        yf = y_coords[i + 1]
        d = math.sqrt((xf - xi) ** 2 + (yf - yi) ** 2)
        tallied_distance += d
        tallied_distances.append(tallied_distance)
    random_distances_along_line = [0]
    for i in range(0, n_points - 2):
        random_distances_along_line.append(random.random() * tallied_distance)
    random_distances_along_line.sort()
    new_x_points = [x_coords[0]]
    new_y_points = [y_coords[0]]
    for i in range(0, len(random_distances_along_line)):
        dt = random_distances_along_line[i]
        for j in range(0, len(tallied_distances) - 1):
            di = tallied_distances[j]
            df = tallied_distances[j + 1]
            if di < dt and dt < df:
                difference = dt - di
                xi = x_coords[j]
                xf = x_coords[j + 1]
                yi = y_coords[j]
                yf = y_coords[j + 1]
                xt = xi + (xf - xi) * difference / (df - di)
                yt = yi + (yf - yi) * difference / (df - di)
                new_x_points.append(xt)
                new_y_points.append(yt)
    new_x_points.append(x_coords[len(x_coords) - 1])
    new_y_points.append(y_coords[len(y_coords) - 1])
    # plt.plot(new_x_points, new_y_points)
    # plt.scatter(new_x_points, new_y_points, s=2)
    # ax = plt.gca()
    # ax.set_aspect('equal')
    # plt.show()
    return new_x_points, new_y_points, n_points


def approximate_coords(x_coords, y_coords, n=4, distance_threshold=0.01):
    # Initialize new lists to store the averaged coordinates
    new_x_coords = []
    new_y_coords = []

    i = 0
    while i < len(x_coords) - 1:
        # Calculate the distance between the current point and the next point
        dist = math.sqrt((x_coords[i + 1] - x_coords[i]) ** 2 + (y_coords[i + 1] - y_coords[i]) ** 2)

        # If the distance is below the threshold, average the points within the window of size n
        if dist < distance_threshold:
            x_window = x_coords[i:i + n]
            y_window = y_coords[i:i + n]

            avg_x = sum(x_window) / len(x_window)
            avg_y = sum(y_window) / len(y_window)

            new_x_coords.append(avg_x)
            new_y_coords.append(avg_y)

            i += n  # Skip the next n points
        else:
            # If the distance is above the threshold, just add the current point
            new_x_coords.append(x_coords[i])
            new_y_coords.append(y_coords[i])

            i += 1  # Move to the next point

    # Append the last point to make sure the contour closes correctly
    new_x_coords.append(x_coords[-1])
    new_y_coords.append(y_coords[-1])

    # Return the new coordinates and the number of points
    n_points = len(new_x_coords)
    return new_x_coords, new_y_coords, n_points
