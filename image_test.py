import argparse
import sys
from ForthBBProtocol import ForthBadge as Badge
from BadgeSerial import def_cmap as badge_colors
#from ForthBBProtocol import pack_rgb
from PIL import Image
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def draw_image_to_badge(image_path,
                        bg_color='green',
                        x_offs=0, y_offs=0,
                        badge=None,
                        show_progress=True,
                        verbose=False):
    if badge is None:
        badge = Badge()

    badge.set_background_color(bg_color)
    im = Image.open(image_path)
    pix = im.load()
    num_pix = im.size[0] * im.size[1]
    cnt = 0

    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            cnt += 1
            # Div by 8 to do rough scaling of 255-0 down to 31-0
            pix_val = [int(c/8) for c in pix[x,y]]
            if verbose:
                print("(%d, %d) = %s" %(x, y, pix_val))
            color = Badge.pack_rgb(*pix_val)
            badge.set_draw_color(color)
            badge.draw_point(x_offs + x,
                             y_offs + y)

            if show_progress:
                num_bars = int(20*(cnt/float(num_pix)))
                print("[%d/%d]|%s%s|" % (cnt, num_pix, ("="*num_bars), "-"*(20-num_bars)), end='\r')
        badge.push_buffer()

    #badge.swap_buffer()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an image to the badge")
    parser.add_argument(dest='image_path', type=str,
                        help='Path to an image file')
    parser.add_argument('-b', '--bg-color', dest='bg_color', type=str,
                        default='green',
                        help='Background color for the image: ' + ", ".join(badge_colors.keys()))
    args = parser.parse_args()

    if args.bg_color not in badge_colors:
        print("'%s' is not a valid color, check --help for colors" % str(args.bg_color))
        sys.exit(1)

    draw_image_to_badge(args.image_path, bg_color=args.bg_color)

