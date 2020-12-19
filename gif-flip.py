#!/usr/bin/env python3

from PIL import Image, ImageOps
from optparse import OptionParser
from sys import exit

# python 3 script to convert an image to a 512x512 flipping gif
# suitable for using as custom emojis in slack
# Ken Mininger, kmininger@us.ibm.com
# October 2020

usage = '''
        Takes an image and resizes to 512x512 (maintaining aspect ratio and quality),
        flips it, applies speed, and saves as an
        animated GIF. If image is smaller than 512x512, it will not resize but
        will flip as-is.

        EXAMPLE: gif-flip.py -i test.jpg -o test.gif -s 100'''


# resize image to 512x512, maintaining aspect ratio and quality
# resize to anything smaller than this and there is quality loss
# if the image is smaller than 512x512, it will not resize
# but will flip (may look weird)
def resize_image(r_image):
    img_height = 512
    img_width = 512
    if (r_image.height <= img_height) or (r_image.width <= img_width):
        return r_image
    if (r_image.width != img_width) & (r_image.height != img_height):
        r2_image = ImageOps.fit(r_image, [img_width, img_height], Image.ANTIALIAS)
        return r2_image
    else:
        return r_image


# flip the image
def flip_image(c_image):
    images = []
    trans_img1 = ImageOps.flip(c_image)
    images.append(trans_img1)
    trans_img2 = ImageOps.mirror(c_image)
    images.append(trans_img2)
    return images


# open image file and convert
# png files are weird
def open_file(option):
    try:
        logo()
        image_open = Image.open(option, 'r')
        print("Opened", option, "for flipping.")
        if (image_open.height < 512) or (image_open.width < 512):
            print("WARNING: Image smaller than 512x512. The flip may look weird.")
        if image_open.format == "PNG":
            print("PNG files are weird. Use another format until a new version is released.")
            exit(1)
        else:
            image_open = image_open.convert("P", palette=Image.ADAPTIVE, colors=256)
            return image_open
    except IOError:
        print("Error: Cannot open input file for reading or input file not found.")
    exit(1)


# gif flip
def logo():
    print("""\
   ________________   _________     
  / ____/  _/ ____/  / ____/ (_)___ 
 / / __ / // /_     / /_  / / / __ \\
/ /_/ // // __/    / __/ / / / /_/ /
\____/___/_/      /_/   /_/_/ .___/ 
                           /_/      """)


# simple error checking
def error_check(infile, flipfile, speed):
    if not infile:
        logo()
        print("Input file not provided: use -i")
        exit(1)
    if not flipfile:
        logo()
        print("Output file not provided: use -o")
        exit(1)
    if not speed:
        logo()
        print("Give me some speed: use -s")
        exit(1)


# flip and save the image
def flippity_flip(image, infile, speed, flipfile):
    print("Flipping", infile, "with speed = ", speed)
    resized = resize_image(image)
    flipped = flip_image(resized)
    try:
        flipped[0].save(flipfile, 'GIF', save_all=True, append_images=flipped[1:],
                        duration=speed,
                        loop=0,
                        optimize=True, quality=100)
        print("Flipping GIF created:", flipfile)
    except IOError:
        print("Error: Cannot open output file for writing")
        exit(1)


# options: input file, output file, and speed
def check_args():
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--infile", dest="infile", help="Picture to spin", type="string")
    parser.add_option("-o", "--flipfile", dest="flipfile", help="Output file (must include .gif)", type="string")
    parser.add_option("-s", "--speed", dest="speed", help="The lower the number, the faster the spin (100 makes a good "
                                                          "clean spin)", type="int")
    (options, args) = parser.parse_args()
    return (options, args)


# main
def main():
    # get the command line arguments
    (options, args) = check_args()

    # ensure all options have been provided
    error_check(options.infile, options.flipfile, options.speed)

    # open the image file for reading and get the image
    img = open_file(options.infile)

    # flip and build the gif
    flippity_flip(img, (options.infile), (options.speed), (options.flipfile))


if __name__ == '__main__':
    main()
