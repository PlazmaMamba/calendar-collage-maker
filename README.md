# Python Image Collage Maker

This Python script provides a comprehensive solution for processing a collection of images within a directory. It automates the task of sorting images by date, correcting their orientation based on EXIF metadata, scaling them down, and dynamically arranging them on a canvas. This tool is ideal for generating organized photo collections, preparing images for digital albums, or any application that requires automated image handling and layout.

## Features

- **Automatic Orientation Correction:** Fixes image rotation according to EXIF metadata to ensure all images are correctly oriented.
- **Image Scaling:** Dynamically scales images down based on the number of images to be placed on a single canvas, maintaining a balance between visibility and layout efficiency.
- **Sort by Date:** Organizes images by the date captured, using EXIF data, to ensure chronological ordering.
- **Dynamic Image Placement:** Calculates the optimal layout for images on a canvas, considering the number of images and their orientations, and places them accordingly.
- **Canvas Generation:** Creates a canvas (or multiple canvases) to host the grouped and processed images, saving the output as PNG files with unique timestamps.

## Dependencies

- Python 3.x
- Pillow (PIL Fork): A Python Imaging Library adds image processing capabilities to your Python interpreter. This script uses Pillow for opening, manipulating, and saving many different image file formats.

To install Pillow, run:

```bash
pip install Pillow
```

## Usage

- **Set up your environment:** Ensure Python 3.x and Pillow are installed.
- **Prepare your images:** Place all images you wish to process in a single directory.
- **Run the script:** Execute the script from your terminal or command prompt.

The script will then process the images, sort them, correct their orientation, scale them down, and arrange them on canvases. Each canvas will be saved with a unique timestamp in the script's running directory.

## Contributing
Feel free to fork this repository and submit pull requests to contribute to this project. For major changes, please open an issue first to discuss what you would like to change.

## To-Do
- [ ] Improve running speed
- [ ] Make the grid layout more flexible
- [ ] Add better support for images with not 4:3 or 3:4 aspect ratios

## License
Distributed under the MIT License. See LICENSE for more information.

## Contact
- Project Link: https://github.com/PlazmaMamba/python-image-collage-maker
- Discord : PlazmaMamba#5365

