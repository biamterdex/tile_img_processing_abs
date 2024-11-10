
# Tile Edge and Corner Detection

This Python project detects and marks tile edges and corners in images. It processes images by detecting lines, extending them, and identifying intersections that represent tile corners. The processed images are then saved with these annotations, making it easier to analyze tiled surfaces or patterns.

## Features

- **Edge Detection**: Detects edges in an image using Canny edge detection after grayscale conversion and Gaussian blurring.
- **Line Detection**: Identifies straight lines using Hough Line Transform, filtering for near-horizontal and near-vertical lines.
- **Line Extension**: Extends detected lines across the image for better corner detection.
- **Corner Detection**: Calculates intersections of extended lines to determine tile corners.
- **Batch Processing**: Processes all images within a folder and saves the processed images with marked edges and corners.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Math, OS, Glob (Standard Libraries)

To install dependencies:

```bash
pip install opencv-python-headless numpy
```

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/biamterdex/tile_img_processing_abs
   cd tile_img_processing_abs
   ```

2. **Set up Input and Output Folders**:
   - Place images to be processed in an input folder (e.g., `media/Tiles/`).
   - Define an output folder where processed images will be saved (e.g., `media/Output_results/`).

3. **Run the Script**:

   ```bash
   python3 tile_corners_detecter.py
   ```

4. **Parameters and Folders**:
   - In `detect_tiles.py`, adjust the paths to match your input and output folders:
     ```python
     input_folder = 'media/Tiles/'  # Your input folder path
     output_folder = 'media/Output_results/'  # Your output folder path
     ```

5. **Processing a Single Image (Optional)**:
   - To process a single image directly, uncomment the example usage line at the end of the script:
     ```python
     detect_tile_edges_and_corners('path/to/image.png', 'path/to/output_image.png')
     ```

## Script Overview

The core functionality is organized in the following functions:

- `line_intersection(line1, line2)`: Calculates the intersection point of two lines.
- `extend_line(line, img_shape)`: Extends a line across the image dimensions.
- `calculate_line_angle(line)`: Calculates the angle of a line in degrees.
- `detect_tile_edges_and_corners(image_path, output_path)`: Main function for edge and corner detection in a single image.
- `process_folder(input_folder, output_folder)`: Processes all images in a specified folder.

## Example

Given a tiled pattern image, the script outputs an annotated image with extended lines and intersections marking tile corners:

| Original Image | Processed Image |
|----------------|-----------------|
| ![Original Image](media\Tiles\tile%20(1).png) | ![Processed Image](media\Output_results\image002.png) |

