
import os, sys
from PIL import Image



def ask_size():
    w=int(input("Enter width: "))
    h=int(input("Enter height: "))
    return w,h


def get_image_path():
    img_path = input("Path: ")
    return img_path


def resize_image(image_path,new_size):
    with Image.open(image_path) as im:
        image_resized = im.resize(new_size)
    return image_resized


def save_new_image(image_resized, image_path):
    image_path = os.path.normpath(image_path)
    root, extension = os.path.splitext(image_path)
    new_file_path = rf"{root}-resized{extension}"  
    image_resized.save(new_file_path)


def resize_image_main_operation():
    new_size = ask_size()
    image_path = get_image_path()
    image_resized = resize_image(image_path, new_size)
    save_new_image(image_resized, image_path)


def create_directory():
    new_directory = input("Enter new directory")
    iterations = 0
    while os.path.isdir(new_directory):
        iterations += 1
        new_directory = new_directory+str(iterations)
    os.makedirs(new_directory, exist_ok=True)
    return new_directory


def downscale_image(image_path, ratio):
    with Image.open(image_path) as im:
        (w,h) = (im.width // ratio, im.height // ratio)
        image_resized = im.resize((w,h))
    return image_resized


def downscale_batch(directory,new_directory,ratio):
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        image_resized = downscale_image(image_path,ratio)
        new_image_path = os.path.join(new_directory, os.path.basename(filename))
        new_image_path = os.path.normpath(new_directory + '/' + os.path.basename(filename))
        save_new_image(image_resized, new_image_path)
        

        
def downscale_main():
    ratio = int(input("Enter ratio: "))
    directory = get_image_path()
    new_directory = create_directory()
    print(new_directory)
    downscale_batch(directory, new_directory,ratio)


def create_canvas(canvas_size):
    canvas = Image.new('RGBA', canvas_size, (255, 255, 255, 255))
    return canvas

def paste_image_centered(canvas, image):
    canvas_width, canvas_height = canvas.size
    image_width, image_height = image.size
    paste_x = (canvas_width - image_width) // 2
    paste_y = (canvas_height - image_height) // 2
    canvas.paste(image, (paste_x, paste_y))
    return canvas

def merge_canvases(canvases):
    widths, heights = zip(*(c.size for c in canvases))
    total_width = max(widths) * 2
    total_height = max(heights) * 2
    merged_canvas = Image.new('RGBA', (total_width, total_height))
    
    # Merge top-left canvas
    merged_canvas.paste(canvases[0], (0, 0))
    
    # Merge top-right canvas
    merged_canvas.paste(canvases[1], (max(widths), 0))
    
    # Merge bottom-left canvas
    merged_canvas.paste(canvases[2], (0, max(heights)))
    
    # Merge bottom-right canvas
    merged_canvas.paste(canvases[3], (max(widths), max(heights)))
    
    return merged_canvas



def scale_image_for_canvas(image, canvas_size):
    width, height = canvas_size
    new_width = int(width * 0.85)
    new_height = int(height * 0.85)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def add_images_to_canvas_corners():
    image_paths = []
    
    for i in range(4):
        image_path = get_image_path()
        image_paths.append(image_path)
    
    canvases = []
    canvas_size = ask_size()
    
    colors = []  
    
    for i in range(4):
        image = Image.open(image_paths[i])
        
        image = scale_image_for_canvas(image, canvas_size)
        canvas = create_canvas(canvas_size)
        canvas = canvas.convert('RGBA')
        
        
        color = input(f"Enter the color for sub-canvas {i+1}: ")
        colors.append(color)
        
        canvas = Image.new('RGBA', canvas.size, colors[i])  
        canvas = paste_image_centered(canvas, image)
        canvases.append(canvas)
        image.close()
        
    
    merged_canvas = merge_canvases(canvases)
    save_new_image(merged_canvas, "merged_canvas.png")
    canvas.close()
    merged_canvas.close()
    
    return merged_canvas





def one_image_debug():
    image_paths = []
    for i in range(1):
        image_path = get_image_path()
        image_paths.append(image_path)
    
    canvases = []
    canvas_size = ask_size()
    
    colors = []  
    
    for i in range(1):
        image = Image.open(image_paths[i])
        
        image = scale_image_for_canvas(image, canvas_size)
        canvas = create_canvas(canvas_size)
        canvas = canvas.convert('RGBA')
        
        
        color = input(f"Enter the color for sub-canvas {i+1}: ")
        colors.append(color)
        
        canvas = Image.new('RGBA', canvas.size, colors[i])  
        canvas = paste_image_centered(canvas, image)
        canvases.append(canvas)
        image.close()
    canvas = create_canvas(canvas_size)
    for i in range(3):
        canvas = canvas.convert('RGBA')
        
        
        color = input(f"Enter the color for sub-canvas {i+2}: ")
        colors.append(color)
        
        canvas = Image.new('RGBA', canvas.size, colors[i+1])  
        canvases.append(canvas)
        
        
    
    merged_canvas = merge_canvases(canvases)
    save_new_image(merged_canvas, "merged_canvas.png")
    canvas.close()
    merged_canvas.close()
    
    return merged_canvas





def add_images_to_canvas_corners_batch():
    image_paths = []
    directory = get_image_path()
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        image_paths.append(image_path)
    
    
    canvases = []
    canvas_size = ask_size()

def get_folder_for_batch():
    image_paths = []
    directory = get_image_path()
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        image_paths.append(image_path)
    return image_paths


def combine_four_images(image_paths, batch_index):
    canvases = []
    canvas_size = 400,300
    
    colors = ['red','green','blue','pink']  
    
    for i in range(4):
        image = Image.open(image_paths[i])
        
        image = scale_image_for_canvas(image, canvas_size)
        canvas = create_canvas(canvas_size)
        canvas = canvas.convert('RGBA')
        
        canvas = Image.new('RGBA', canvas.size, colors[i])  
        canvas = paste_image_centered(canvas, image)
        canvases.append(canvas)
        image.close()
        
    merged_canvas = merge_canvases(canvases)
    save_new_image(merged_canvas, f"merged_canvas_{batch_index}.png")  
    canvas.close()
    merged_canvas.close()
    

def combine_four_images_batch():
    image_paths = get_folder_for_batch()
    for i in range(0, len(image_paths), 4):
        batch = image_paths[i:i+4]
        if len(batch) == 4:
            combine_four_images(batch,i//4 )
        else:
            
            if len(batch) == 1:
                image = Image.open(batch[0])
                canvas_size = ask_size()
                image = scale_image_for_canvas(image, canvas_size)
                canvas = create_canvas(canvas_size)
                canvas = canvas.convert('RGBA')
                color = 'red'
                canvas = Image.new('RGBA', canvas.size, color)
                canvas = paste_image_centered(canvas, image)
                save_new_image(canvas, "merged_canvas-one-image.png")
                image.close()
                canvas.close()
            elif len(batch) == 2:
                # Combine two images
                image1 = Image.open(batch[0])
                image2 = Image.open(batch[1])
                canvas_size = ask_size()
                image1 = scale_image_for_canvas(image1, canvas_size)
                image2 = scale_image_for_canvas(image2, canvas_size)
                canvas = create_canvas(canvas_size)
                canvas = canvas.convert('RGBA')
                color = 'green'
                canvas = Image.new('RGBA', canvas.size, color)
                canvas = paste_image_centered(canvas, image1)
                canvas = paste_image_centered(canvas, image2)
                save_new_image(canvas, "merged_canvas-two-image.png")
                image1.close()
                image2.close()
                canvas.close()
            elif len(batch) == 3:
                # Combine three images
                image1 = Image.open(batch[0])
                image2 = Image.open(batch[1])
                image3 = Image.open(batch[2])
                canvas_size = ask_size()
                image1 = scale_image_for_canvas(image1, canvas_size)
                image2 = scale_image_for_canvas(image2, canvas_size)
                image3 = scale_image_for_canvas(image3, canvas_size)
                canvas = create_canvas(canvas_size)
                canvas = canvas.convert('RGBA')
                color = 'blue'
                canvas = Image.new('RGBA', canvas.size, color)
                canvas = paste_image_centered(canvas, image1)
                canvas = paste_image_centered(canvas, image2)
                canvas = paste_image_centered(canvas, image3)
                save_new_image(canvas, "merged_canvas-three-image.png")
                image1.close()
                image2.close()
                image3.close()
                canvas.close()


    



















