import numpy as np
import cv2


def average_lines(image, lines):
    left_lines = []
    right_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        if x2 == x1:
            continue  # Skip vertical lines

        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        if slope < -0.3:
            left_lines.append((slope, intercept))
        elif slope > 0.3:
            right_lines.append((slope, intercept))

    def make_line(image, params):
        slope, intercept = np.mean(params, axis=0)

        h = image.shape[0]
        y1 = h
        y2 = int(h * 0.6)

        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        return [(x1, y1, x2, y2)]

    averaged = []

    if left_lines:
        averaged.append(make_line(image, left_lines))

    if right_lines:
        averaged.append(make_line(image, right_lines))

    return averaged


def detect_lanes(image_path):
    """
    Detect lane lines from an image.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    output = image.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges
    edges = cv2.Canny(blur, 50, 150)

    # Region of Interest
    height, width = edges.shape

    mask = np.zeros_like(edges)

    polygon = np.array([[
        (0, height),
        (width, height),
        (int(width * 0.60), int(height * 0.60)),
        (int(width * 0.40), int(height * 0.60))
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)

    cropped = cv2.bitwise_and(edges, mask)

    # Hough Line Transform
    lines = cv2.HoughLinesP(
        cropped,
        rho=2,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=40,
        maxLineGap=5
    )

    if lines is None:
        print("No lane lines detected.")
        return output

    averaged_lines = average_lines(image, lines)

    for line in averaged_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return output


if __name__ == "__main__":
    result = detect_lanes("sample_road.jpg")

    cv2.imshow("Lane Detection", result)
    cv2.imwrite("lane_output.jpg", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()