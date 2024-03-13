import os, sys
from PIL import Image, ExifTags, ImageOps
from datetime import datetime
import concurrent.futures


#Get the directory of the image files
def get_directory():
    
    directory = input(r"Enter directory: ")
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    image_paths = [
        os.path.join(directory, filename) for filename in os.listdir(directory)
        if os.path.splitext(filename)[1].lower() in image_extensions
    ]
    return image_paths


#Correctly rotate the image based on the metadata
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


#Get the date of the image and rotate it correctly
def get_date_and_rotate(image_path):
    with Image.open(image_path) as image:
        image.load()
        corrected_image = fix_rotation_of_image_from_metadata(image)
        corrected_image.load()
        try:
            exif = corrected_image.getexif()
            date = exif[36867] if exif else '0000:00:00 00:00:00'  # Default to a very early date if not available
            return corrected_image.copy(), date
        except KeyError:
            return corrected_image.copy(), '0000:00:00 00:00:00'    


#Sort the the rotated images by date
def sort_images_by_date(image_paths):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        images_and_dates = list(executor.map(get_date_and_rotate, image_paths))
    sorted_images_and_dates = sorted(filter(lambda x: x[0] is not None, images_and_dates), key=lambda x: x[1])
    sorted_images = [img for img, _ in sorted_images_and_dates]
    return sorted_images


#Scale the image based on the orientation
def scale_image_concurrently(image, scale_size=0.85):
    if get_image_rotation(image) == 1:  # Landscape
        new_size = tuple(int(size*scale_size) for size in image.size)
        return ImageOps.fit(image, new_size, Image.LANCZOS)
    else:  # Portrait
        new_size = tuple(int(size*scale_size) for size in image.size)
        return ImageOps.fit(image, new_size, Image.LANCZOS)
        

#Get the orientation of the image, 1 for landscape and 0 for portrait
def get_image_rotation(image):
    return 1 if image.size[0] > image.size[1] else 0


#Group the images based on the number of images per canvas
def group_images(images, group_size):
    
    return [images[i:i + group_size] for i in range(0, len(images), group_size)]


#Create the canvas for the images
def create_canvas(grouped_images, LANDSCAPE_HEIGHT, LANDSCAPE_WIDTH):
    canvases = []
    for group in grouped_images:
        canvas = Image.new('RGBA', (LANDSCAPE_WIDTH*2, LANDSCAPE_HEIGHT*2))
        canvases.append(canvas)
    return canvases


#Calculate the centers of the images to paste them on the canvas
def calculate_centers(canvas_width, canvas_height, num_images, margin=0.1):
    canvas_width = canvas_width *2
    canvas_height = canvas_height *2
    centers = []
    num_rows = int(round((num_images / (canvas_width / canvas_height)) ** 0.5))
    num_columns = -(-num_images // num_rows)  
    partition_width = int(canvas_width / num_columns)
    partition_height = int(canvas_height / num_rows)
    for row in range(num_rows):
        for col in range(num_columns):
            center_x = int((col + 0.5) * partition_width)
            center_y = int((row + 0.5) * partition_height)
            centers.append((center_x, center_y))
    return centers


#Save the canvas with a timestamped filename
def save_canvas_concurently(canvas, index):
    """Save a single canvas with a timestamped filename."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{index}_{timestamp}.png"
    canvas.save(filename)
    print(f"Saved: {filename}")
    

#Process the group of images and paste them on the canvas
def process_group_and_paste(canvas, images, scale_factor,LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, PORTRAIT_WIDTH, PORTRAIT_HEIGHT,index):
    scaled_images = [scale_image_concurrently(image, scale_factor) for image in images]
    centers = calculate_centers(LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, len(images))
    positions = []
    for center, scaled_image in zip(centers, scaled_images):
            top_left_x = center[0] - scaled_image.width // 2
            top_left_y = center[1] - scaled_image.height // 2
            positions.append((top_left_x, top_left_y))
    for position, scaled_image in zip(positions, scaled_images):
        canvas.paste(scaled_image, position)
    save_canvas_concurently(canvas, index)


#Process the entire group of images and paste them on canvases
def paste_images_on_canvas_concurrently(canvases, grouped_images, LANDSCAPE_HEIGHT, LANDSCAPE_WIDTH, PORTRAIT_HEIGHT, PORTRAIT_WIDTH, num_images):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = []

        for i, canvas in enumerate(canvases):
            images = grouped_images[i]
            total_images = len(images)
            scale_factor = max(0.45, 1 - total_images * 0.05)

            task = executor.submit(process_group_and_paste, canvas, images, scale_factor, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, PORTRAIT_WIDTH, PORTRAIT_HEIGHT,i)
            tasks.append(task)

        concurrent.futures.wait(tasks)
    return canvases
   

#Main function to create the final images
def final_images():
    image_paths = get_directory()
    image_height = int(input("Enter Image Height "))
    image_width = int(input("Enter Width "))
    number_of_images = int(input("Enter number of images per canvas "))
    images = sort_images_by_date(image_paths)
    canvases = create_canvas(group_images(images,number_of_images),image_height,image_width)
    paste_images_on_canvas_concurrently(canvases, group_images(images,number_of_images),image_height,image_width,image_width,image_height,number_of_images)
    

#Run the main function
if __name__ == "__main__":
    final_images()
    




    





    
    




