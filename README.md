A collection of small image manipulation scripts with Pillow.
The most useful one is combine_four_images_batch()
The goal of this function is to go through all images in a folder, and combine them 4 by 4 into a single large image, that you can use for a calendar for example.
If you want to change the colors, you can modify the colors = ['red','green','blue','pink']  list in the combine_four_images() function. The controls for the resolution of the smaller images are also located
in this function under canvas_size = 400,300 .
