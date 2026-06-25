import cv2
import numpy as np

print("Lane Detection Started")


def region_of_interest(img):

    height, width = img.shape

    polygon = np.array([
        [
            (0, height),
            (width, height),
            (int(width * 0.75), int(height * 0.55)),
            (int(width * 0.25), int(height * 0.55))
        ]
    ], np.int32)

    mask = np.zeros_like(img)

    cv2.fillPoly(mask, polygon, 255)

    return cv2.bitwise_and(img, mask)


def average_lines(image, lines):

    left_fit = []
    right_fit = []

    if lines is None:
        return None, None

    for line in lines:

        x1, y1, x2, y2 = line.reshape(4)

        if x1 == x2:
            continue

        slope = np.polyfit((x1, x2), (y1, y2), 1)[0]
        intercept = np.polyfit((x1, x2), (y1, y2), 1)[1]

        if slope < -0.4:
            left_fit.append((slope, intercept))

        elif slope > 0.4:
            right_fit.append((slope, intercept))

    left_lane = None
    right_lane = None

    if len(left_fit) > 0:
        left_lane = np.average(left_fit, axis=0)

    if len(right_fit) > 0:
        right_lane = np.average(right_fit, axis=0)

    return left_lane, right_lane


def make_points(image, lane):

    slope, intercept = lane

    y1 = image.shape[0]
    y2 = int(y1 * 0.6)

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return [x1, y1, x2, y2]


def detect_lanes(image_path):

    image = cv2.imread(image_path)

    if image is None:
        print("Image not found")
        return

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    white_lower = np.array([0, 0, 180])
    white_upper = np.array([255, 60, 255])

    yellow_lower = np.array([15, 80, 80])
    yellow_upper = np.array([35, 255, 255])

    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    mask = cv2.bitwise_or(white_mask, yellow_mask)

    lane_only = cv2.bitwise_and(image, image, mask=mask)

    gray = cv2.cvtColor(lane_only, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 50, 150)

    roi = region_of_interest(edges)

    lines = cv2.HoughLinesP(
        roi,
        2,
        np.pi / 180,
        threshold=50,
        minLineLength=40,
        maxLineGap=100
    )

    # DEBUGGING
    if lines is None:
        print("No lines detected")
    else:
        print("Number of lines detected:", len(lines))

    left_lane, right_lane = average_lines(image, lines)

    output = image.copy()

    # LEFT LANE (GREEN)
    if left_lane is not None:

        x1, y1, x2, y2 = make_points(image, left_lane)

        print("Left Lane Detected")

        cv2.line(
            output,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            8
        )
    else:
        print("Left Lane Not Detected")

    # RIGHT LANE (BLUE)
    if right_lane is not None:

        x1, y1, x2, y2 = make_points(image, right_lane)

        print("Right Lane Detected")

        cv2.line(
            output,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            8
        )
    else:
        print("Right Lane Not Detected")

    # ROAD EDGES (RED)

    h, w = image.shape[:2]

    cv2.line(
        output,
        (0, h),
        (int(w * 0.30), int(h * 0.60)),
        (0, 0, 255),
        4
    )

    cv2.line(
        output,
        (w, h),
        (int(w * 0.70), int(h * 0.60)),
        (0, 0, 255),
        4
    )

    cv2.imwrite("lane_output.jpg", output)

    print("Lane detection completed")
    print("Saved as lane_output.jpg")

    cv2.imshow("Lane Detection", output)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":

    detect_lanes("sample_road.jpg")