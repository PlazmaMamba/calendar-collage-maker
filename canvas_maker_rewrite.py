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
    directory = input(r"Enter directory: ")
    image_paths = [os.path.join(directory, filename) for filename in os.listdir(directory)]
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
    

def scale_down_image(image, LANDSCAPE_SIZE, scale_size=0.85):
    new_size = tuple(int(size*scale_size) for size in LANDSCAPE_SIZE)
    return image.resize(new_size)

    



def sort_images_by_date(image_paths):
    def get_date(image):
        try:
            exif = image.getexif()
            return exif[36867] if exif else '0000:00:00 00:00:00'  # Default to a very early date if not available
        except KeyError:
            return '0000:00:00 00:00:00'

    # Open each image, fix its rotation, then store it with its path
    images = []
    for path in image_paths:
        image = Image.open(path)
        corrected_image = fix_rotation_of_image_from_metadata(image)  # Correcting the image orientation
        images.append((corrected_image, path))

    # Sort images by the date extracted from their EXIF data
    images.sort(key=lambda img: get_date(img[0]))

    # Return the list of sorted images without paths, as paths are no longer needed beyond this point
    return [img for img, _ in images]


def get_image_rotation(image):
    return 1 if image.size[0] > image.size[1] else 0
    
def calculate_rotation_layout(images):
    rotation_layout = 0
    for image in images:
        rotation = get_image_rotation(image)
        rotation_layout += rotation
    return rotation_layout



    
def group_images(images, group_size):
    """
    Groups images into chunks of a specified size.
    """
    return [images[i:i + group_size] for i in range(0, len(images), group_size)]

#create a canvas, if case for each possible combination of images
def create_canvas(grouped_images, LANDSCAPE_HEIGHT, LANDSCAPE_WIDTH):
    canvases = []
    for group in grouped_images:
        canvas = Image.new('RGBA', (LANDSCAPE_WIDTH*2, LANDSCAPE_HEIGHT*2))
        canvases.append(canvas)
    return canvases


def calculate_centers(canvas_width, canvas_height, num_images, margin=0.1):
    canvas_width = canvas_width *2
    canvas_height = canvas_height *2
    centers = []
    num_rows = int(round((num_images / (canvas_width / canvas_height)) ** 0.5))
    num_columns = -(-num_images // num_rows)  # Ceiling division
    partition_width = int(canvas_width / num_columns)
    partition_height = int(canvas_height / num_rows)
    for row in range(num_rows):
        for col in range(num_columns):
            center_x = int((col + 0.5) * partition_width)
            center_y = int((row + 0.5) * partition_height)
            centers.append((center_x, center_y))
    return centers







def paste_images_dynamically_on_canvas(canvases, grouped_images, LANDSCAPE_HEIGHT, LANDSCAPE_WIDTH, PORTRAIT_HEIGHT, PORTRAIT_WIDTH, num_images):
    # Assuming calculate_centers and scale_down_image functions are correct
    for i, canvas in enumerate(canvases):
        images = grouped_images[i]
        scaled_images = []
        # Dynamically adjust scale based on the number of images
        total_images = len(images)
        # Example dynamic scaling calculation (this formula is illustrative; adjust based on your needs)
        scale_factor = max(0.45, 1 - total_images * 0.05)
        for image in images:
            if get_image_rotation(image) == 1:  # Landscape
                scaled_image = scale_down_image(image, (LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT), scale_factor)
            else:  # Portrait
                scaled_image = scale_down_image(image, (PORTRAIT_WIDTH, PORTRAIT_HEIGHT),scale_factor)
            scaled_images.append(scaled_image)

        centers = calculate_centers(LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, len(images))

        positions = []
        for center, scaled_image in zip(centers, scaled_images):
            top_left_x = center[0] - scaled_image.width // 2
            top_left_y = center[1] - scaled_image.height // 2
            positions.append((top_left_x, top_left_y))

        # Debug output
        #for position in positions:
            #print("Position for pasting:", position)

        for j, scaled_image in enumerate(scaled_images):
            canvas.paste(scaled_image, positions[j])


    return canvases



    


def save_canvas(canvases):
    # Get the current timestamp to append to the filename for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save each canvas with a timestamp to ensure uniqueness
    for i, canvas in enumerate(canvases):
        filename = f"canvas_{i}_{timestamp}.png"  # Append the timestamp to the filename
        canvas.save(filename)
        print(f"Saved: {filename}")













def final_images():
    image_paths = get_directory()
    image_height = int(input("Enter Image Height "))
    image_width = int(input("Enter Width "))
    number_of_images = int(input("Enter number of images per canvas "))
    images = sort_images_by_date(image_paths)
    canvases = create_canvas(group_images(images,number_of_images),image_height,image_width)
    canvases = paste_images_dynamically_on_canvas(canvases, group_images(images,number_of_images),image_height,image_width,image_width,image_height,number_of_images)
    save_canvas(canvases)

if __name__ == "__main__":
    final_images()




    





    
    




