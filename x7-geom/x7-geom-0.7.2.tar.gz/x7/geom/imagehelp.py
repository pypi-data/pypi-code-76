# coding: utf-8

"""
Helper routines for PIL.Image.Image
"""

from PIL import Image, ImagePalette


def image_info_palette(pal_im: Image.Image):
    pal = pal_im.palette
    pal_colors = pal_im.getpalette()
    colors = pal_im.getcolors()
    print('Colors:', colors)
    print('Palette:')
    n_channels = len(pal.mode)
    print('  Mode:', pal.mode, ' (%d channels)' % n_channels)
    print('  Raw: ', pal.rawmode)
    pal_len = len(pal.palette) // n_channels
    print('  Len: ', pal_len)
    show_bytes = True
    if show_bytes:
        total = -10
        for idx in range(len(pal.palette)):
            if pal.palette[idx]:
                total += 1
                if total >= 10:
                    if total == 10:
                        print('   ...')
                else:
                    print('   %d %d' % (idx, pal.palette[idx]))
    total = 0
    show_for_weird_bug = False
    if show_for_weird_bug:
        # Sometimes, the palette is RGB, RGB instead of RR..RRGG..GGBB..BB
        for n in range(pal_len):
            base = n * n_channels
            c = tuple([pal_colors[base + cn] for cn in range(n_channels)])
            if any(c):
                total += 1
                if total >= 20:
                    if total == 20:
                        print('  ...')
                else:
                    print('  %3d: %s' % (n, c))
    else:
        for n in range(pal_len):
            c = tuple([pal_colors[n + cn * 256] for cn in range(n_channels)])
            if any(c):
                total += 1
                if total >= 20:
                    if total == 20:
                        print('  ...')
                else:
                    print('  %3d: %s' % (n, c))


def image_fix_palette(im: Image.Image):
    """Set all non-zero alpha values to 255"""
    assert im.palette.mode == 'RGBA'
    if not isinstance(im.palette.palette, bytearray):
        im.palette.palette = bytearray(im.palette.palette)
    pal = im.palette.palette
    color = (64, 128, 255, 255)
    for n in range(0, 256):
        idx = n * 4
        alpha = pal[idx + 3]
        if alpha and alpha != 255:
            for c in range(3):
                pal[idx + c] = int(color[c] * alpha / 255)
            pal[idx + 3] = 255
    im.palette.dirty = 1


def image_info(im: Image.Image):
    bbox = im.getbbox()
    xs, ys = im.size
    print('Image: %s %s' % (im.mode, bbox or '(empty image)'))
    print('Info: %s' % im.info)
    image_info_palette(im)
    zero = im.getpixel((0, 0))
    # zero = 0 if len(im.mode) == 1 else (0,)*len(im.mode)
    print('Zero: ', zero)
    bbox = bbox or (0, 0, 0, 0)
    low_y = bbox[1]
    for row in range(max(0, low_y - 2), min(ys, low_y + 4)):
        data = []
        for x in range(min(256, xs)):
            val = im.getpixel((x, row))
            if not data:
                data.append(val)
            elif val != zero:
                data.append(val)
            elif data[-1] == zero:
                data.append('...')
            elif data[-1] != '...':
                data.append(val)
        data = ' '.join(str(d) for d in data)
        print('Row %d: %s' % (row, data))


def rgba_to_transparent(im, colors=256):
    # See: https://stackoverflow.com/questions/46850318/transparent-background-in-gif-using-python-imageio
    assert im.mode == 'RGBA'

    alpha = im.getchannel('A')

    # Convert the image into P mode but use one less color in the palette to reserve for transparent index
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=colors - 1)

    cheap_hack = True
    if cheap_hack:
        im.info['transparency'] = im.getpixel((0, 0))  # Assume upper-left pixel should be transparent
    # im.palette.palette = bytearray(im.palette.palette)
    # im.palette.palette[3] = 255
    # im.palette.dirty = 1
    else:
        # Set all pixel values below 128 to 255 , and the rest to 0
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)

        # Paste the color of index 255 and use alpha as a mask
        im.paste(colors - 1, mask=mask)
        im.paste(colors - 1, box=(50, 50, 100, 100))

        # The transparency index is colors-1
        im.info['transparency'] = colors - 1

    return im


# noinspection PyShadowingNames
def rgb_to_transparent(im, colors=256, palette_image=None):
    # See: https://stackoverflow.com/questions/46850318/transparent-background-in-gif-using-python-imageio
    assert im.mode == 'RGB'

    if palette_image:
        im = im.quantize('P', palette=palette_image, dither=Image.NONE)
    else:
        im = im.convert('P', palette=Image.ADAPTIVE, colors=colors)
        # A bit of laziness.  Turns out for white images, the ADAPTIVE palette is [almost-white, black],
        # so we can turn it into [black, white] fairly easily.
        im = im.remap_palette([1, 0])  # Rewrite the image with 0 as black and 1 as white
        im.palette.palette = b'\xFF' * 768  # Now, make the palette all white
        im.palette.getcolor((0, 0, 0))  # Except for first entry as black

    im.info['transparency'] = im.getpixel((0, 0))  # Assume upper-left pixel should be transparent

    return im


def palette_image(empty_image=False):
    """Return a 16-place palette image"""
    im = Image.new('P', (1024, 64))
    pal: ImagePalette.ImagePalette = im.palette
    pal.palette = b'\x00' * 768
    pal.getcolor((0, 0, 0))
    pal.getcolor((255, 255, 255))
    if not empty_image:
        for c in range(256):
            ox = c * 4
            im.paste(c, (ox, 0, ox + 4, 64))
            if c > len(pal.colors):
                pal.getcolor((c, (c + 128) % 256, (500 - c) % 256))
    im.load()
    return im


def test_gif():
    images = [Image.new('RGB', (50, 50), c) for c in ['white', 'red', 'blue', 'green', 'black', 'grey']]
    # save_and_show(images)
    images[0].save('animationt.gif', save_all=True, append_images=images[1:])


def test_all():
    test_gif()


# test_image_helpers()


def test_palette():
    im = palette_image()
    print(len(im.palette.colors))
    im.palette.colors = {}
    # im.show()
    unmapped: Image.Image = Image.open('/tmp/kltv_unmapped.png')
    colors = {}
    for color in unmapped.getdata():
        colors.setdefault(color, 0)
        colors[color] += 1
    print(len(colors))
    all_colors = list(reversed(sorted([(v, k) for k, v in colors.items()])))
    for idx, (count, color) in enumerate(all_colors[:10]):
        print('%3d: %6d %s' % (idx, count, color))
    for idx, (count, color) in enumerate(all_colors[:256]):
        im.palette.getcolor(color)
    im.show()


if __name__ == '__main__':
    test_palette()
# test_all()
