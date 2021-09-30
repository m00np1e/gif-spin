Python 3 script for creating an annoying spinning GIF.

Suitable for Slack (or whatever else).

Takes an image (file) as input, converts the image to a 120x120 thumbnail, spins clockwise with specified speed, and saves the spinning or bouncing GIF as output (file).

If the image is smaller than 80x80, it will work but may look weird.

USAGE:

Do some stuff with the image: gif-spin.py -i [input file] -o [output file] -s [speed]

Where [speed] is an integer. 50-100 makes a good clean spin. 20 is turbo spin.

Requires: https://github.com/python-pillow/Pillow
