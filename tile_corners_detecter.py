import cv2
import numpy as np
import math
import os
import glob

def line_intersection(line1, line2):
    """Calculate the intersection point of two lines given by endpoints."""
    x1, y1, x2, y2 = map(float, line1)
    x3, y3, x4, y4 = map(float, line2)
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return None  # Parallel lines
    px_numerator = (x1 * y2 - y1 * x2) * (x3 - x4) - \
                   (x1 - x2) * (x3 * y4 - y3 * x4)
    py_numerator = (x1 * y2 - y1 * x2) * (y3 - y4) - \
                   (y1 - y2) * (x3 * y4 - y3 * x4)
    px = px_numerator / denominator
    py = py_numerator / denominator
    return int(px), int(py)

def extend_line(line, img_shape):
    """Extend a line across the image dimensions."""
    x1, y1, x2, y2 = line
    if x2 - x1 == 0:  # Vertical line
        return (x1, 0, x2, img_shape[0] - 1)
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    y_start = int(intercept)
    y_end = int(slope * (img_shape[1] - 1) + intercept)
    return (0, y_start, img_shape[1] - 1, y_end)

def calculate_line_angle(line):
    """Calculate the angle of a line in degrees."""
    x1, y1, x2, y2 = map(float, line)
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return angle

def detect_tile_edges_and_corners(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    
    # Convert to grayscale and apply Gaussian blur for noise reduction
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Enhance contrast and apply Canny edge detection
    gray = cv2.equalizeHist(gray)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform with adjusted parameters
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=100, maxLineGap=10)
    
    # Check if any lines were detected
    if lines is None:
        print("No lines detected in the image.")
        return

    # Filter lines based on angle and length
    line_image = image.copy()
    filtered_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Calculate the angle in degrees
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        # Only keep lines that are close to horizontal or vertical
        if abs(angle) < 10 or abs(angle) > 80:
            # Calculate line length
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if length > 100:  # Only keep lines longer than 100 pixels
                # Only add lines that are not too close to existing ones
                too_close = any(
                    abs(x1 - ux1) < 100 and abs(y1 - uy1) < 100 and abs(x2 - ux2) < 100 and abs(y2 - uy2) < 100
                    for ux1, uy1, ux2, uy2 in filtered_lines
                )
                if not too_close:
                    filtered_lines.append((x1, y1, x2, y2))

    lines = np.array(filtered_lines)

    extended_lines = []
    line_angles = []

    # Extend each detected line across the image dimensions
    for line in lines:
        extended_line = extend_line(line, image.shape)
        extended_lines.append(extended_line)
        angle = calculate_line_angle(extended_line)
        line_angles.append(angle)
        cv2.line(line_image, (extended_line[0], extended_line[1]), (extended_line[2], extended_line[3]), (0, 255, 0), 1)

    # Calculate intersections of extended lines to find tile corners
    intersections = []
    for i, line1 in enumerate(extended_lines):
        angle1 = line_angles[i]
        for j, line2 in enumerate(extended_lines):
            if i >= j:
                continue
            angle2 = line_angles[j]
            # Check if the lines are approximately perpendicular
            angle_diff = abs(angle1 - angle2)
            angle_diff = angle_diff % 180  # Normalize angle difference
            if abs(angle_diff - 90) > 10:  # Allow a tolerance of ±10 degrees
                continue
            pt = line_intersection(line1, line2)
            if pt is not None:
                x, y = pt
                # Check if the point is within the image bounds
                if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                    intersections.append((x, y))
    
    # Draw detected intersections (corners) on the image
    for x, y in intersections:
        cv2.circle(line_image, (x, y), 5, (255, 0, 0), -1)

    # Save the output image with extended lines and corners
    cv2.imwrite(output_path, line_image)
    print(f"Output saved to {output_path}")


def process_folder(input_folder, output_folder):
    """Process all images in the specified folder."""
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Supported image extensions
    image_extensions = ('*.jpg', '*.jpeg', '*.png')

    # Get a list of all image files in the input folder
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))

    # Check if there are any images to process
    if not image_files:
        print(f"No images found in the folder {input_folder}.")
        return

    # Process each image
    for image_path in image_files:
        # Get the base name of the image file
        base_name = os.path.basename(image_path)
        # Construct the output file path
        output_path = os.path.join(output_folder, f"processed_{base_name}")
        print(f"Processing {image_path}...")
        # Call the processing function
        detect_tile_edges_and_corners(image_path, output_path)

# Example usage
if __name__ == "__main__":
    input_folder = 'media/Tiles/'  # Replace with your input folder path
    output_folder = 'media/Output_results/'  # Replace with your output folder path
    process_folder(input_folder, output_folder)
