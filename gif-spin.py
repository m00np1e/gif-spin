#!/usr/bin/env python3

# python 3 script to convert an image to a 120x120
# clockwise spinning gif
# suitable for use with custom emotes in slack
# Ken Mininger, kmininger@us.ibm.com
# October 2021

from PIL import Image, ImageOps
from sys import exit
import argparse


def check_args():
    parser = argparse.ArgumentParser(
        description="Creates a clockwise spinning GIF.", prog="GIF-Manip",
        usage="%(prog)s "
              "[options]")
    parser.add_argument("-i", help="Input file - The file you want to spin.",
                        required=True)
    parser.add_argument("-o", help="Output file - Must specify .gif extension. If not, I'll add it for you.", required=True)
    parser.add_argument("-s", help="Spin speed (50 is a good clean spin, 20 is turbo spin).", type=int, required=True)
    args1 = parser.parse_args()
    return (args1)


# open image file
def open_file(option):
    try:
        doing = "spinning."
        image_open = Image.open(option, 'r')
        print("Opened", option, "for", doing)
        if (image_open.height < 80) or (image_open.width < 80):
            print("WARNING: Image smaller than 80x80. The", (doing[:-1]), "may look weird.")
        if image_open.format == "PNG":
            bg_color = (0, 0, 0)
            rgb_img = rem_trans(image_open, bg_color)
            return (rgb_img)
        else:
            image_open = image_open.convert("P", palette=Image.ADAPTIVE, colors=256)
            return image_open
    except IOError:
        print("Error: Cannot open input file for reading or input file not found.")
    exit(1)


# convert png to rgba image
def rem_trans(img, color_bg):
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        alpha = img.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", img.size, color_bg + (255,))
        bg.paste(img, mask=alpha)
        return bg
    else:
        return img


# resize image
def resize_image(r_image):
    img_height = 120
    img_width = 120
    reduce_percent = .4
    if (r_image.height <= img_height) or (r_image.width <= img_width):
        return r_image
    if (r_image.width != img_width) & (r_image.height != img_height):
        # r2_image = ImageOps.fit(r_image, [img_width, img_height], Image.ANTIALIAS)
        new_image_height = int(reduce_percent * r_image.height)
        new_image_width = int(reduce_percent * r_image.width)
        r2_image = ImageOps.fit(r_image, [new_image_width, new_image_height], Image.ANTIALIAS)
        return r2_image
    else:
        return r_image


# rotate the image clockwise
def clockwise(c_image):
    images = []
    degrees = -1
    while degrees >= -360:
        trans_img = c_image.rotate(degrees)
        images.append(trans_img)
        degrees -= 20
    return images


def spin_clockwise(image, infile, speed, spinfile):
    print("Spinning", infile, "clockwise with speed =", str(speed) + ".")
    resized = resize_image(image)
    clockwised = clockwise(resized)
    try:
        clockwised[0].save(spinfile, 'GIF', save_all=True, append_images=clockwised[1:],
                           duration=speed,
                           loop=0,
                           optimize=True, quality=100)
        print("Spinning GIF created:", spinfile)
    except IOError:
        print("Error: Cannot open output file for spinning.")
        exit(1)


def gif_file(extension):
    if not extension.endswith('.gif'):
        filename_new = extension + ".gif"
        return filename_new
    else:
        return extension



# main
def main():
    # get args
    (args) = check_args()

    # check that .gif is appended to the -o argument
    new_output = gif_file(args.o)

    # open the file and get the image
    img = open_file(args.i)

    # spin it
    spin_clockwise(img, args.i, args.s, new_output)


if __name__ == '__main__':
    main()
