import os, sys
from PIL import Image, ExifTags
from datetime import datetime

LANDSCAPE_IMG_HEIGHT = 3000
LANDSCAPE_IMG_WIDTH = 4000
PORTRAIT_IMG_HEIGHT = 4000
PORTRAIT_IMG_WIDTH = 3000

LANDSCAPE_SIZE = (LANDSCAPE_IMG_WIDTH, LANDSCAPE_IMG_HEIGHT)
PORTRAIT_SIZE = (PORTRAIT_IMG_WIDTH, PORTRAIT_IMG_HEIGHT)

def get_directory():
    directory = input("Enter directory: ")
    image_paths = []
    
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        image_paths.append(image_path)
    return image_paths

def fix_rotation_of_image_from_metadata(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(image._getexif().items())

        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass
    return image
    

def scale_down_landscape_image(image, LANDSCAPE_SIZE, scale_size=0.85):
    new_size = tuple(int(size*scale_size) for size in LANDSCAPE_SIZE)
    image_resized = image.resize(new_size)
    return image_resized

def scale_down_portrait_image(image, PORTRAIT_SIZE, scale_size=0.85):
    new_size = tuple(int(size*scale_size) for size in PORTRAIT_SIZE)
    image_resized = image.resize(new_size)
    return image_resized

def sort_images_by_date(image_paths):
    images = []
    for image_path in image_paths:
        image = Image.open(image_path)
        image = fix_rotation_of_image_from_metadata(image)
        images.append(image)

    try:
        images.sort(key=lambda x: x._getexif()[36867])
    
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass
    return images

def get_image_rotation(image):
    if image.size[0] > image.size[1]:
        return 1
    else:
        return 0
    
def calculate_rotation_layout(images):
    rotation_layout = 0
    for image in images:
        rotation = get_image_rotation(image)
        rotation_layout += rotation
    return rotation_layout


    
def group_images_in_group_of_4(images):
    grouped_images = [images[i:i+4] for i in range(0, len(images), 4)]
    return grouped_images

def group_images_in_group_of_6(images):
    grouped_images = [images[i:i+6] for i in range(0, len(images), 6)]
    return grouped_images

#create a canvas, if case for each possible combination of images
def create_canvas(grouped_images, LANDSCAPE_HEIGHT, LANDSCAPE_WIDTH):
    canvases = []
    for group in grouped_images:
        canvas = Image.new('RGBA', (LANDSCAPE_WIDTH*2, LANDSCAPE_HEIGHT*2))
        canvases.append(canvas)
    return canvases

def paste_images_on_canvas(canvases, grouped_images, LANDSCAPE_HEIGHT, LANDSCAPE_WIDTH, PORTRAIT_HEIGHT, PORTRAIT_WIDTH):
    for i, canvas in enumerate(canvases):
        images = grouped_images[i]
        scaled_images = []
        for image in images:
            # Determine scaling based on image rotation
            if get_image_rotation(image) == 1:  # Assuming 1 means landscape
                scaled_image = scale_down_landscape_image(image, (LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT),0.9)
            else:  # Assuming 0 means portrait
                scaled_image = scale_down_portrait_image(image, (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), 0.75)
            scaled_images.append(scaled_image)

        # Correctly calculate the centering offset for each scaled image
        #offsets = [(LANDSCAPE_WIDTH / 4 - scaled_image.width / 2, LANDSCAPE_HEIGHT / 4 - scaled_image.height / 2) for scaled_image in scaled_images]

        # Adjust the calculation of positions for each image to be correctly centered in each quadrant
        # Define the center points for each image
        centers = [
            (2000, 1500),  # Center for first image
            (6000, 1500),  # Center for second image
            (2000, 4500),  # Center for third image
            (6000, 4500)   # Center for fourth image
        ]

        positions = []
        # Calculate the top-left corner for each image to center it at the specified points
        for center, image in zip(centers, scaled_images):
            top_left_x = center[0] - image.width // 2
            top_left_y = center[1] - image.height // 2
            positions.append((top_left_x, top_left_y))
            
        # Paste each scaled image at the calculated centered position
        for j, scaled_image in enumerate(scaled_images):
            canvas.paste(scaled_image, (int(positions[j][0]), int(positions[j][1])))

    return canvases


def paste_six_images_on_canvas(canvases, grouped_images, LANDSCAPE_HEIGHT, LANDSCAPE_WIDTH, PORTRAIT_HEIGHT, PORTRAIT_WIDTH):
    for i, canvas in enumerate(canvases):
        images = grouped_images[i]
        scaled_images = []
        for image in images:
            # Determine scaling based on image rotation
            if get_image_rotation(image) == 1:  # Assuming 1 means landscape
                scaled_image = scale_down_landscape_image(image, (LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT), 0.8)
            else:  # Assuming 0 means portrait
                scaled_image = scale_down_portrait_image(image, (PORTRAIT_WIDTH, PORTRAIT_HEIGHT), 0.75)
            scaled_images.append(scaled_image)

        # Define the center points for each image in a 2x3 grid layout
        centers = [
        # Row 1
        (1333, 1500),  # First column, first row
        (4000, 1500),  # Second column, first row
        (6667, 1500),  # Third column, first row
        # Row 2
        (1333, 4500),  # First column, second row
        (4000, 4500),  # Second column, second row
        (6667, 4500),  # Third column, second row
        ]

        positions = []
        # Calculate the top-left corner for each image to center it at the specified points
        for center, image in zip(centers, scaled_images):
            top_left_x = center[0] - image.width // 2
            top_left_y = center[1] - image.height // 2
            positions.append((top_left_x, top_left_y))
            
        # Paste each scaled image at the calculated centered position
        for j, scaled_image in enumerate(scaled_images):
            canvas.paste(scaled_image, (int(positions[j][0]), int(positions[j][1])))

    return canvases


def save_canvas(canvases):
    # Get the current timestamp to append to the filename for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save each canvas with a timestamp to ensure uniqueness
    for i, canvas in enumerate(canvases):
        filename = f"canvas_{i}_{timestamp}.png"  # Append the timestamp to the filename
        canvas.save(filename)
        print(f"Saved: {filename}")


def main():
    image_paths = get_directory()
    images = sort_images_by_date(image_paths)
    #canvases = create_canvas(group_images_in_group_of_4(images), LANDSCAPE_IMG_HEIGHT, LANDSCAPE_IMG_WIDTH)
    #canvases = paste_images_on_canvas(canvases, group_images_in_group_of_4(images), LANDSCAPE_IMG_HEIGHT, LANDSCAPE_IMG_WIDTH, PORTRAIT_IMG_HEIGHT, PORTRAIT_IMG_WIDTH)
    #save_canvas(canvases)
    canvases = create_canvas(group_images_in_group_of_6(images), LANDSCAPE_IMG_HEIGHT, LANDSCAPE_IMG_WIDTH)
    canvases = paste_six_images_on_canvas(canvases, group_images_in_group_of_6(images), LANDSCAPE_IMG_HEIGHT, LANDSCAPE_IMG_WIDTH, PORTRAIT_IMG_HEIGHT, PORTRAIT_IMG_WIDTH)
    save_canvas(canvases)
main()

                    
                    

    #case 4 portrait

    #case 2 landscape, 2 portrait

    #case 3 landscape 1 portrait

    #case 3 portrait 1 landscape

    
    




