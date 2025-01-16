from numpy import array
from sys import stdout

from PIL import Image


def convert_qr_to_ascii(image, invert):
    image_array = array(image.getdata())

    width = image.size[0]
    height = image.size[1]

    # get offset
    offset = 0
    while image_array[offset * width + offset][0] == 255:
        offset += 1

    # get scale
    scale = 1
    while image_array[(offset + scale) * width + (offset + scale)][0] == 0:
        scale += 1

    # resize
    image = image.resize((width // scale, height // scale), Image.Resampling.NEAREST)
    image_array = array(image.getdata())
    width = image.size[0]
    height = image.size[1]

    # inverted colors
    if invert:
        image_array = 255 - image_array
    # print image
    with stdout as f:
        for i in range(height):
            for j in range(width):
                if image_array[i * width + j][0] < 128:
                    print("██", end='')
                else:
                    print("  ", end='')
            print(file=f)
