from asyncio import sleep

import cv2
import numpy as np
import matplotlib.pyplot as plt
from cobot.rodri import draw
from vector.reduced_coords import reduced_coords


def show_points(x_coords_local, y_coords_local):
    plt.figure()
    plt.scatter(x_coords_local, y_coords_local, c='blue', marker='o')
    plt.title('Reduced X, Y Coordinates of All Contours')
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.grid(True)
    plt.show()


# Load the image
image = cv2.imread('/home/jorgesuarez/PycharmProjects/Robotica-Brazo/vector/formitas.png')

image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("gray", gray)
cv2.waitKey(0)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply edge detection (Canny) with different thresholds if necessary
edges = cv2.Canny(blurred, 100, 200)

cv2.imshow("edges", edges)
cv2.waitKey(0)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(f'Number of contours: {len(contours)}')

# Draw contours on the image
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

cv2.imshow("contours", image)
cv2.waitKey(0)

# Define the frame limits (in centimeters)
frame_top_left = (78, 43)  # x=78, y=43
frame_bottom_right = (23, -35)  # x=23, y=-35

# Extract frame width and height in real-world units (centimeters)
frame_width_cm = frame_top_left[0] - frame_bottom_right[0]  # x difference
frame_height_cm = frame_top_left[1] - frame_bottom_right[1]  # y difference

# Get image dimensions (in pixels)
image_height, image_width = image.shape[:2]

# Initialize lists to hold all contours' reduced coordinates
all_x_coords = []
all_y_coords = []
n = 0

# Iterate over each contour
for contour in contours:
    x_coords = []
    y_coords = []

    for point in contour:
        x_pixel, y_pixel = point[0]

        # Scale pixel coordinates to real-world coordinates in centimeters
        x_cm = frame_top_left[0] - (x_pixel / image_width) * frame_width_cm
        y_cm = frame_top_left[1] - (y_pixel / image_height) * frame_height_cm

        # Convert centimeters to meters
        x_m = x_cm / 100.0
        y_m = y_cm / 100.0

        # Append the real-world coordinates to the lists
        x_coords.append(x_m)
        y_coords.append(y_m)

        # Draw the contour on the image (optional)
        # cv2.circle(image, (x_pixel, y_pixel), 1, (0, 255, 0), -1)

    # Apply reduced_coords to the current contour
    reduced_x, reduced_y, n_points = reduced_coords(x_coords, y_coords)
    reduced_x.append(reduced_x[0])
    reduced_y.append(reduced_y[0])
    show_points(reduced_x, reduced_y)
    draw(reduced_x, reduced_y)
    n += n_points

print(f'Total number of points after reduction: {n}')

# Display the image with detected curves
cv2.imshow('Detected Curves', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
