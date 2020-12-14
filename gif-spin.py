#!/usr/bin/env python3

from PIL import Image, ImageOps
from optparse import OptionParser
from sys import exit

# python 3 script to convert an image to a 512x512 spinning gif
# suitable for using as custom emojis in slack
# Ken Mininger, kmininger@us.ibm.com
# October 2020

usage = '''
        Takes an image and resizes to 512x512 (maintaining aspect ratio and quality),
        rotates clockwise or counterclockwise, applies speed, and saves as an
        animated GIF.
        
        EXAMPLE: gif-spin.py -i test.jpg -o test.gif -d c -s 100'''


# resize image to 512x512, maintaining aspect ratio and quality
# anything smaller than this and there is quality loss
def resize_image(r_image):
    img_height = 512
    img_width = 512
    if (r_image.width != img_width) & (r_image.height != img_height):
        r2_image = ImageOps.fit(r_image, [512, 512], Image.ANTIALIAS)
        return r2_image
    else:
        return r_image


# rotate the image clockwise
def clockwise(c_image):
    images = []
    images.append(c_image)
    trans_img1 = c_image.rotate(-90)
    images.append(trans_img1)
    trans_img2 = c_image.rotate(-180)
    images.append(trans_img2)
    trans_img3 = c_image.rotate(-270)
    images.append(trans_img3)
    return images


# rotate the image counterclockwise
def counterclockwise(cc_image):
    images = []
    images.append(cc_image)
    trans_img1 = cc_image.rotate(90)
    images.append(trans_img1)
    trans_img2 = cc_image.rotate(180)
    images.append(trans_img2)
    trans_img3 = cc_image.rotate(270)
    images.append(trans_img3)
    return images


# open image file and convert, keeping the quality of the original file
def open_file(option):
    try:
        image_open = Image.open(option, 'r').convert("P", palette=Image.ADAPTIVE, colors=256)
        logo()
        print("Opened", option, "for spinning.")
        return image_open
    except IOError:
        print("Error: Cannot open input file for reading or input file not found.")
    exit(1)


# gif spin
def logo():
    print("""\
                   ________________   _____            
                  / ____/  _/ ____/  / ___/____  (_)___ 
                 / / __ / // /_      \__ \/ __ \/ / __ \\
                / /_/ // // __/     ___/ / /_/ / / / / /
                \____/___/_/       /____/ .___/_/_/ /_/ 
                                       /_/              """)


# simple error checking
def error_check(infile, spinfile, speed, direction):
    if not infile:
        logo()
        print("Input file not provided: -i")
        exit(1)
    if not spinfile:
        logo()
        print("Output file not provided: -o")
        exit(1)
    if not speed:
        logo()
        print("Give me some speed: -s")
        exit(1)
    if not direction:
        logo()
        print("Give me a direction (cc or c): -d")
        exit(1)


# spin clockwise and save the image
def spin_clockwise(image, infile, speed, spinfile):
    print("Spinning", infile, "clockwise with speed = ", speed)
    resized = resize_image(image)
    clockwised = clockwise(resized)
    try:
        clockwised[0].save(spinfile, 'GIF', save_all=True, append_images=clockwised[1:],
                           duration=speed,
                           loop=0,
                           optimize=True, quality=100)
        print("Spinning GIF created:", spinfile)
    except IOError:
        print("Error: Cannot open output file for writing")
        exit(1)


# spin counterclockwise and save the image
def spin_counterclockwise(image, infile, speed, spinfile):
    print("Spinning", infile, "counterclockwise with speed = ", speed)
    resized = resize_image(image)
    ccwised = counterclockwise(resized)
    try:
        ccwised[0].save(spinfile, 'GIF', save_all=True, append_images=ccwised[1:], duration=speed,
                        loop=0,
                        optimize=True, quality=100)
        print("Spinning GIF created: ", spinfile)
    except IOError:
        print("Error: Cannot open output file for writing")
        exit(1)


# options: input file, output file, speed, and direction
def check_args():
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--infile", dest="infile", help="Picture to spin", type="string")
    parser.add_option("-o", "--spinfile", dest="spinfile", help="Output file (must include .gif)", type="string")
    parser.add_option("-s", "--speed", dest="speed", help="The lower the number, the faster the spin (100 makes a good "
                                                          "clean spin)", type="int")
    parser.add_option("-d", "--direction", dest="direction", help="Counterclockwise (cc) or clockwise (c)",
                      type="string")
    (options, args) = parser.parse_args()
    return (options, args)


# main
def main():
    # get the command line arguments
    (options, args) = check_args()

    # ensure all options have been provided
    error_check(options.infile, options.spinfile, options.speed, options.direction)

    # open the image file for reading and get the image
    img = open_file(options.infile)

    # determine direction and build the gif
    if options.direction == "c":
        spin_clockwise(img, (options.infile), (options.speed), (options.spinfile))
    elif options.direction == "cc":
        spin_counterclockwise(img, (options.infile), (options.speed), (options.spinfile))
    else:
        print("You provided a direction, but it wasn't c or cc.")
        exit(1)


if __name__ == '__main__':
    main()
