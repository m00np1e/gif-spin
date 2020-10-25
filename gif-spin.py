from PIL import Image
from optparse import OptionParser
from sys import exit

# options
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
img = Image.open((options.infile), 'r').convert("P", palette=Image.ADAPTIVE, colors=256)

# build the animated gif
images = []
images.append(img)
trans_img1 = img.transpose(Image.ROTATE_90)
images.append(trans_img1)
trans_img2 = img.transpose(Image.ROTATE_180)
images.append(trans_img2)
trans_img3 = img.transpose(Image.ROTATE_270)
images.append(trans_img3)

# save the animated gif
images[0].save(options.spinfile, 'GIF', save_all=True, append_images=images[1:], duration=100, loop=0, optimize=True)