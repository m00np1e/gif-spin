from PIL import Image, ImageOps
from optparse import OptionParser
from sys import exit

# python 3 program to convert an image to a 512x512 spinning gif
# suitable for using as custom emojis in slack
# Ken Mininger, kmininger@us.ibm.com
# October 2020

# options, input and output file
parser = OptionParser()
parser.add_option("-i", "--infile", dest="infile", type="string")
parser.add_option("-o", "--spinfile", dest="spinfile", type="string")
(options, args) = parser.parse_args()

# simple error checking
if not options.infile:
    parser.error("Input file not provided")
    exit(1)
if not options.spinfile:
    parser.error("Output file not provided")
    exit(1)

# open image file and convert to keep the quality of the original file
try:
    img = Image.open((options.infile), 'r').convert("P", palette=Image.ADAPTIVE, colors=256)
except IOError:
    print("Error: Cannot open input file for reading or input file not found")
    exit(1)

# resize image to a square 512x512 thumbnail, maintaining aspect ratio and quality
# anything smaller than this and there is quality loss
img_height = 512
img_width = 512
if (img.width != img_width) & (img.height != img_height):
    thumbnail = ImageOps.fit(img, [512, 512], Image.ANTIALIAS)
else:
    thumbnail = img

# rotate the images and build the animated gif
images = []
images.append(thumbnail)
trans_img1 = thumbnail.transpose(Image.ROTATE_90)
images.append(trans_img1)
trans_img2 = thumbnail.transpose(Image.ROTATE_180)
images.append(trans_img2)
trans_img3 = thumbnail.transpose(Image.ROTATE_270)
images.append(trans_img3)

# save the animated gif
try:
    images[0].save(options.spinfile, 'GIF', save_all=True, append_images=images[1:], duration=100, loop=0, optimize=True, quality = 100)
except IOError:
    print("Error: Cannot open output file for writing")
    exit(1)