import cv2
import numpy as np


def region_of_interest(image):
    """
    Masks the image to keep only the road region.
    """
    height, width = image.shape

    mask = np.zeros_like(image)

    polygon = np.array([[
        (0, height),
        (width, height),
        (int(width * 0.6), int(height * 0.6)),
        (int(width * 0.4), int(height * 0.6))
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)

    return cv2.bitwise_and(image, mask)


def average_lines(image, lines):
    """
    Average all detected lane lines into one left and one right lane.
    """

    left_fit = []
    right_fit = []

    if lines is None:
        return []

    # Convert to (N,4)
    lines = np.array(lines).reshape(-1, 4)

    for x1, y1, x2, y2 in lines:

        if x1 == x2:
            continue

        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        if slope < -0.3:
            left_fit.append((slope, intercept))
        elif slope > 0.3:
            right_fit.append((slope, intercept))

    lane_lines = []

    if left_fit:
        lane_lines.append(make_line(image, np.mean(left_fit, axis=0)))

    if right_fit:
        lane_lines.append(make_line(image, np.mean(right_fit, axis=0)))

    return lane_lines


def make_line(image, line):
    """
    Converts slope and intercept into line coordinates.
    """

    slope, intercept = line

    height = image.shape[0]

    y1 = height
    y2 = int(height * 0.6)

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return (x1, y1, x2, y2)


def detect_lanes(image_path):
    """
    Detect lane lines from an image.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    output = image.copy()

    # -------------------------
    # Step 1: Grayscale
    # -------------------------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # -------------------------
    # Step 2: Gaussian Blur
    # -------------------------
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # -------------------------
    # Step 3: Edge Detection
    # -------------------------
    edges = cv2.Canny(blur, 50, 150)

    # -------------------------
    # Step 4: ROI
    # -------------------------
    cropped = region_of_interest(edges)

    # -------------------------
    # Step 5: Hough Transform
    # -------------------------
    lines = cv2.HoughLinesP(
        cropped,
        rho=2,
        theta=np.pi / 180,
        threshold=50,
        minLineLength=40,
        maxLineGap=100
    )

    # -------------------------
    # Step 6: Average lanes
    # -------------------------
    averaged_lines = average_lines(image, lines)

    # -------------------------
    # Step 7: Draw lanes
    # -------------------------
    for x1, y1, x2, y2 in averaged_lines:
        cv2.line(
            output,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            5
        )

    return output


if __name__ == "__main__":

    print("Lane Detection Started...")

    result = detect_lanes("sample_road.jpg")

    cv2.imwrite("lane_output.jpg", result)

    print("Lane Detection Completed.")
    print("Output saved as lane_output.jpg")

    cv2.imshow("Original Image", cv2.imread("sample_road.jpg"))
    cv2.imshow("Detected Lanes", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()