#!/usr/bin/env python3

from PIL import Image, ImageOps
from optparse import OptionParser
from sys import exit


# python 3 program to convert an image to a 512x512 spinning gif
# suitable for using as custom emojis in slack
# Ken Mininger, kmininger@us.ibm.com
# October 2020


# function to resize image to 512x512, maintaining aspect ratio and quality
# anything smaller than this and there is quality loss
def resize_image(r_image):
    img_height = 512
    img_width = 512
    if (r_image.width != img_width) & (r_image.height != img_height):
        r2_image = ImageOps.fit(r_image, [512, 512], Image.ANTIALIAS)
        return r2_image
    else:
        return r_image


# function to rotate the image clockwise
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


# function to rotate the image counterclockwise
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


# function to open image file and convert, keeping the quality of the original file
def open_file(option):
    try:
        image_open = Image.open(option, 'r').convert("P", palette=Image.ADAPTIVE, colors=256)
        print("Opened", option, "for spinning")
        return image_open
    except IOError:
        print("Error: Cannot open input file for reading or input file not found")
    exit(1)


# main
def main():
    # options: input file, output file, speed, and direction
    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="infile", help="Picture to spin", type="string")
    parser.add_option("-o", "--spinfile", dest="spinfile", help="Output file (must include .gif)", type="string")
    parser.add_option("-s", "--speed", dest="speed", help="The lower the number, the faster the spin (100 makes a good "
                                                          "clean spin)", type="int")
    parser.add_option("-d", "--direction", dest="direction", help="Counterclockwise (cc) or clockwise (c)",
                      type="string")
    (options, args) = parser.parse_args()
    # simple error checking
    if not options.infile:
        parser.error("Input file not provided")
        exit(1)
    if not options.spinfile:
        parser.error("Output file not provided")
        exit(1)
    if not options.speed:
        parser.error("Give me some speed")
        exit(1)
    if not options.direction:
        parser.error("Give me a direction (cc or c)")

    # open the image file for reading and get the image
    img = open_file(options.infile)

    # determine direction and build the gif
    # clockwise spin
    if options.direction == "c":
        print("Spinning", options.infile, "clockwise with speed = ", options.speed)
        resized = resize_image(img)
        clockwised = clockwise(resized)
        try:
            clockwised[0].save(options.spinfile, 'GIF', save_all=True, append_images=clockwised[1:],
                               duration=options.speed,
                               loop=0,
                               optimize=True, quality=100)
            print("Spinning GIF created:", options.spinfile)
        except IOError:
            print("Error: Cannot open output file for writing")
            exit(1)
    # counterclockwise spin
    else:
        print("Spinning", options.infile, "counterclockwise with speed = ", options.speed)
        resized = resize_image(img)
        ccwised = counterclockwise(resized)
        try:
            ccwised[0].save(options.spinfile, 'GIF', save_all=True, append_images=ccwised[1:], duration=options.speed,
                            loop=0,
                            optimize=True, quality=100)
            print("Spinning GIF created: ", options.spinfile)
        except IOError:
            print("Error: Cannot open output file for writing")
            exit(1)


if __name__ == '__main__':
    main()
