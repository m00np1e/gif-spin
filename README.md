# gif-spin
Python 3 script to create a spinning GIF for Slack (or whatever else).

Takes an image (file) as input, converts the image to a 512x512 thumbnail, applies speed and rotation, and saves the spinning GIF as output (file).

USAGE:

gif-spin.py -i [input file] -o [output file] -s [speed] -d [direction]

or

gif-spin.py --infile [input file] --spinfile [output file] --speed [speed] -- [direction]

Where [speed] is an integer. The lower the number, the faster the spin. 100 makes a good clean spin.

Where [direction] is either c for clockwise rotation or cc for counterclockwise rotation.

Requires: https://github.com/python-pillow/Pillow



# gif-spin-strobe
Same as above but gives you the option of a red, yellow, or orange annoying strobe effect.

Just add an -f argument and the color of your choice: red, yellow, orange.
