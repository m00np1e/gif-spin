#!/usr/bin/env python3

from PIL import Image, ImageOps
from optparse import OptionParser
from sys import exit

# python 3 script to convert an image to a 512x512 spinning gif
# with an annoying color (red, yellow, or orange) strobe
# suitable for using as custom emojis in slack
# Ken Mininger, kmininger@us.ibm.com
# October 2020

usage = '''
        Takes an image and resizes to 512x512 (maintaining aspect ratio and quality),
        rotates clockwise or counterclockwise, applies speed, applies strobe color
        and saves as an animated GIF.

        EXAMPLE: gif-spin.py -i test.jpg -o test.gif -d c -s 100 -f orange'''


# resize image to 512x512, maintaining aspect ratio and quality
# anything smaller than this and there is quality loss
def resize_image(r_image):
    img_height = 512
    img_width = 512
    if (r_image.height <= 512) or (r_image.width <= 512):
        return r_image
    if (r_image.width != img_width) & (r_image.height != img_height):
        r2_image = ImageOps.fit(r_image, [512, 512], Image.ANTIALIAS)
        return r2_image
    else:
        return r_image


# gif spin
def logo():
    print("""\
   ________________   _____       _          _____ __             __       
  / ____/  _/ ____/  / ___/____  (_)___     / ___// /__________  / /_  ___ 
 / / __ / // /_      \__ \/ __ \/ / __ \    \__ \/ __/ ___/ __ \/ __ \/ _ \\
/ /_/ // // __/     ___/ / /_/ / / / / /   ___/ / /_/ /  / /_/ / /_/ /  __/
\____/___/_/       /____/ .___/_/_/ /_/   /____/\__/_/   \____/_.___/\___/ 
                       /_/                                                 
           """)


# rotate the image clockwise and apply the strobe color
def clockwise(c_image, color):
    images = []
    if color == "red":
        img = Image.new('RGB', (512, 512), (255, 0, 0))
    elif color == "yellow":
        img = Image.new('RGB', (512, 512), (255, 255, 0))
    elif color == "orange":
        img = Image.new('RGB', (512, 512), (255, 140, 0))
    else:
        print("You specified a weird or unsupported color. Try again.")
        exit(1)
    images.append(c_image)
    trans_img1 = c_image.rotate(-90)
    images.append(trans_img1)
    images.append(img)
    trans_img2 = c_image.rotate(-180)
    images.append(trans_img2)
    images.append(img)
    trans_img3 = c_image.rotate(-270)
    images.append(trans_img3)
    images.append(img)
    return images


# rotate the image counterclockwise and apply the strobe color
def counterclockwise(cc_image, color):
    images = []
    if color == "red":
        img = Image.new('RGB', (512, 512), (255, 0, 0))
    elif color == "yellow":
        img = Image.new('RGB', (512, 512), (255, 255, 0))
    elif color == "orange":
        img = Image.new('RGB', (512, 512), (255, 140, 0))
    else:
        print("You specified a weird or unsupported color. Try again.")
        exit(1)
    images.append(cc_image)
    trans_img1 = cc_image.rotate(90)
    images.append(trans_img1)
    images.append(img)
    trans_img2 = cc_image.rotate(180)
    images.append(trans_img2)
    images.append(img)
    trans_img3 = cc_image.rotate(270)
    images.append(trans_img3)
    images.append(img)
    return images


# open image file and convert, keeping the quality of the original file
def open_file(option):
    try:
        logo()
        image_open = Image.open(option, 'r')
        print("Opened", option, "for spinning.")
        if (image_open.height < 512) or (image_open.width < 512):
            print("WARNING: Image smaller than 512x512. The spin may look weird.")
        if image_open.format == "PNG":
            print("PNG files are weird. Use another format until a new version is released.")
            exit(1)
        else:
            image_open = image_open.convert("P", palette=Image.ADAPTIVE, colors=256)
            return image_open
    except IOError:
        print("Error: Cannot open input file for reading or input file not found.")
    exit(1)


# simple error checking
def error_check(infile, spinfile, speed, direction, flash):
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
    if not flash:
        logo()
        print("Flash color? red, yellow, or orange: -f")
        exit(1)


# spin clockwise and save the image
def spin_clockwise(image, infile, speed, spinfile, flash):
    resized = resize_image(image)
    clockwised = clockwise(resized, flash)
    print("Spinning", infile, "clockwise with speed = ", speed, "and strobing", flash)
    try:
        clockwised[0].save(spinfile, 'GIF', save_all=True, append_images=clockwised[1:],
                           duration=speed,
                           loop=0,
                           optimize=True, quality=100)
        print("Spinning GIF created:", spinfile)
    except IOError:
        print("Error: Cannot open output file for writing.")
        exit(1)


# spin counterclockwise and save the image
def spin_counterclockwise(image, infile, speed, spinfile, flash):
    resized = resize_image(image)
    ccwised = counterclockwise(resized, flash)
    print("Spinning", infile, "counterclockwise with speed = ", speed, "and strobing", flash)
    try:
        ccwised[0].save(spinfile, 'GIF', save_all=True, append_images=ccwised[1:], duration=speed,
                        loop=0,
                        optimize=True, quality=100)
        print("Spinning GIF created: ", spinfile)
    except IOError:
        print("Error: Cannot open output file for writing.")
        exit(1)


# options: input file, output file, speed, and direction
def check_args():
    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="infile", help="Picture to spin", type="string")
    parser.add_option("-o", "--spinfile", dest="spinfile", help="Output file (must include .gif)", type="string")
    parser.add_option("-s", "--speed", dest="speed", help="The lower the number, the faster the spin (100 makes a good "
                                                          "clean spin)", type="int")
    parser.add_option("-d", "--direction", dest="direction", help="Counterclockwise (cc) or clockwise (c)",
                      type="string")
    parser.add_option("-f", "--flash_color", dest="flash", help="Flash color: red, yellow, or orange", type="string")
    (options, args) = parser.parse_args()
    return (options, args)


# main
def main():
    # get the command line arguments
    (options, args) = check_args()

    # ensure all options have been provided
    error_check(options.infile, options.spinfile, options.speed, options.direction, options.flash)

    # open the image file for reading and get the image
    img = open_file(options.infile)

    # determine direction and build the gif
    if options.direction == "c":
        spin_clockwise(img, (options.infile), (options.speed), (options.spinfile), (options.flash))
    elif options.direction == "cc":
        spin_counterclockwise(img, (options.infile), (options.speed), (options.spinfile), (options.flash))
    else:
        print("You provided a direction, but it wasn't c or cc.")
        exit(1)


if __name__ == '__main__':
    main()
