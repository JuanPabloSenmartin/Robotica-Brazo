import cv2
import numpy as np

# Open the computer's camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('Camera Feed - Press "C" to Capture', frame)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # If 'c' is pressed, capture the frame
    if key == ord('c'):
        # Convert the captured frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply edge detection (Canny)
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # Iterate over each contour
        for contour in contours:
            for point in contour:
                x, y = point[0]
                # Print the coordinates of the curve
                print(f'Curve coordinates: x={x}, y={y}')
                # Draw the contour on the image (optional)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        # Display the captured frame with contours
        cv2.imshow('Captured Frame with Contours', frame)

    # If 'q' is pressed, exit the loop
    elif key == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
