# coding: utf-8
"""
Demo of creating an animated GIF from a sequence of images

* Based in part on the blog post "Vector Animations with Python" by @Zulko
  (http://zulko.github.io/blog/2014/09/20/vector-animations-with-python/)
* Adapted for Pythonista/iOS by Luke Taylor (forum post: https://forum.omz-software.com/topic/2052/gif-art-in-python)
"""

from __future__ import absolute_import
import sys
import bisect
from PIL import Image
from math import sin, cos, tau, radians

from x7.geom import imagehelp
from .typing import *
from .colors import PensByShape, PenBrush
from .drawing import DrawingContext, bbox_max
from .transform import Transform
from .geom import *
from .model import *
from . import platform
import numpy as np

TMP_ANIM = '/tmp/anim.gif' if sys.platform == 'darwin' else 'anim.gif'


def single(im, color='black'):
    """Return a single color image as big as im"""
    return Image.new('RGBA', im.size, color=color)


def composed(im, color='white'):
    return Image.alpha_composite(single(im, color), im)


def getalpha(im: Image.Image):
    """get alpha channel in ios/darwin independent way"""
    assert im.mode.endswith('A')
    return im.split()[-1]


class Animation(object):
    """Class to animate Point objects"""

    # TODO - update approach
    # 		t - basic anim time from 0..1
    # 		t_mod - funcs to reshape t
    # 		xygen - funcs to shape t or t_mod to xy over -1,1 range
    # 		ptgen - for points
    # 		cvgen - curves
    # Note: Returning None means to hide the object (Morph only).  See hide_if()

    def __init__(self, point):
        self.orig = Point(*point.xy())  # Remember original position
        self.point = point

    def update(self, t):
        """Update point/points based on func(t)"""
        raise NotImplementedError('%s.update' % self.__class__.__name__)

    @staticmethod
    def identity():
        """Return an identity mapping for t, wrapping inner"""

        def func(t):
            return t

        return func

    @staticmethod
    def identity_xy():
        """Return t unchanged if (tx, ty).  Map scalar to (t, t)."""

        def func(t):
            return t if isinstance(t, tuple) else (t, t)

        return func

    @staticmethod
    def xy(x_func=lambda t: t, y_func=lambda t: t):
        """Combine separate scale funcs into xy style function"""

        assert isinstance(x_func(0), Number)
        assert isinstance(y_func(0), Number)

        def func(t):
            return x_func(t), y_func(t)

        return func

    @staticmethod
    def ramp_up(start=0.25, end=0.75):
        """Return a ramp 0 before start, 0..1, 1 after end, wrapping inner"""

        return Animation.interpolate([(0, 0), (start, 0), (end, 1), (1, 1)])

    @staticmethod
    def ramp_down(start=0.25, end=0.75):
        """Return a ramp 1 before start, 1..0, 0 after end, wrapping inner"""

        return Animation.interpolate([(0, 1), (start, 1), (end, 0), (1, 0)])

    @staticmethod
    def interpolate(curve: List[Tuple[Number, Number]]):
        """Interpolate along points [(t,val)...]"""
        time, value = zip(*curve)
        time = np.array(time, dtype=float)
        value = np.array(value, dtype=float)

        def func(t):
            if isinstance(t, tuple):
                tx, ty = t
                return np.interp(tx, time, value), np.interp(ty, time, value)
            else:
                return np.interp(t, time, value)

        return func

    @staticmethod
    def periodic(trig_func, frequency=1.0, offset=0.0, scale=1.0, shift=0.0):
        """Return trig_func(frequency*t+radians(offset))*scale+shift"""

        offset = radians(offset)

        def func(t):
            t *= tau * frequency + offset
            return trig_func(t) * scale + shift

        return func

    @staticmethod
    def sin(frequency=1.0, offset=0.0, scale=1.0, shift=0.0):
        """Return sin(frequency*t+radians(offset))*scale+shift"""
        return Animation.periodic(sin, frequency, offset, scale, shift)

    @staticmethod
    def cos(frequency=1.0, offset=0.0, scale=1.0, shift=0.0):
        """Return cos(frequency*t+radians(offset))*scale+shift"""
        return Animation.periodic(cos, frequency, offset, scale, shift)

    @staticmethod
    def sin_cos(frequency=1.0, offset=0.0, scale=1.0, shift=0.0):
        """Return sin, cos"""

        offset = radians(offset)

        def func(t):
            t *= tau * frequency + offset
            return sin(t) * scale + shift, cos(t) * scale + shift

        return func

    @staticmethod
    def hide_if(func, threshold=0):
        """Return None (hidden) if func(t) is below threshold"""

        def inner(t):
            val = func(t)
            if val < threshold:
                return None
            else:
                return val

        return inner

    @staticmethod
    def plot(funcs: List[Tuple[str, Callable]], start=0.0, end=1.0):
        """Plot a list of (tag, func) for debugging assistance"""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        step = 0.01
        t = np.arange(start, end + step, step)
        for tag, func in funcs:
            data = list(map(func, t))
            if isinstance(data[0], tuple):
                data_x, data_y = zip(*data)
                ax.plot(t, data_x, label=tag + '.x')
                ax.plot(t, data_y, label=tag + '.y')
            else:
                ax.plot(t, data, label=tag)

        # ax.set(xlabel='time (s)', ylabel='voltage (mV)', title='About as simple as it gets, folks')
        xticks, xticklabels = zip(*[(n / 20.0, '' if n % 2 == 1 else str(n / 20.0)) for n in range(21)])
        ax.update(dict(xticks=xticks, xticklabels=xticklabels))
        ax.grid()
        ax.legend()
        plt.show()


class AnimationGeneric(Animation):
    """Class to animate Point objects"""

    def __init__(self, point: BasePoint, func: Callable):
        if not isinstance(point, Point):
            raise ValueError('Can only animate Point objects, not %s' % point)
        super().__init__(point)
        self.func = func

    def update(self, t):
        """Update point/points based on func(t)"""
        self.point.setxy(*self.func(t, self.orig, self.point))


class AnimationLinear(Animation):
    """Animate from point to target as t goes from 0 to 1"""

    def __init__(self, point: BasePoint, target: Point):
        if not isinstance(point, Point):
            raise ValueError('Can only animate Point objects, not %s' % point)
        super().__init__(point)
        assert isinstance(target, BasePoint)
        self.target = target

    def update(self, t):
        orig_x, orig_y = self.orig.xy()
        targ_x, targ_y = self.target.xy()
        tx, ty = t if isinstance(t, tuple) else (t, t)
        sx, sy = 1 - tx, 1 - ty
        self.point.setxy(sx * orig_x + tx * targ_x, sy * orig_y + ty * targ_y)


class AnimationLinearFunc(AnimationLinear):
    """Animate from point to target as t goes from 0 to 1"""

    def __init__(self, point: BasePoint, target: Point, func: Callable):
        super().__init__(point, target)
        self.func = func

    def update(self, t):
        super().update(self.func(t))


class AnimationSinusoidal(Animation):
    """Animate from point to target and back as t goes from 0 to 1"""

    def __init__(self, point: BasePoint, target: Point, frequency=1.0, offset=0):
        if not isinstance(point, Point):
            raise ValueError('Can only animate Point objects, not %s' % point)
        super().__init__(point)
        self.target = target
        self.frequency = frequency
        self.offset = offset

    def update(self, t):
        t = (1.0 - cos(t * tau * self.frequency + self.offset * tau / 360)) * 0.5
        ox, oy = self.orig.xy()
        tx, ty = self.target.xy()
        s = 1 - t
        self.point.setxy(s * ox + t * tx, s * oy + t * ty)


class AnimationCircular(Animation):
    """Animate in circle around original point"""

    def __init__(self, point: BasePoint, radius, frequency, offset=0):
        if not isinstance(point, Point):
            raise ValueError('Can only animate Point objects, not %s' % point)
        super().__init__(point)
        self.radius = radius
        self.frequency = frequency
        self.offset = offset

    def update(self, t):
        ox, oy = self.orig.xy()
        theta = t * tau * self.frequency + self.offset
        self.point.setxy(ox + self.radius * sin(theta), oy + self.radius * cos(theta))


class AnimationHolder(object):
    """Just an empty object to serve as global holder"""

    def __init__(self):
        self.animations: List[Animation] = []

    def add(self, animation: Animation):
        self.animations.append(animation)

    def update(self, t):
        for animation in self.animations:
            animation.update(t)


class MorphError(Exception):
    pass


class Morph(Animation):
    def __init__(self, model: Group, source: ElemCurve, target: ElemCurve, t_func: Callable, force=True):
        super().__init__(Point(0, 0))
        self.model = model
        if force:
            if len(source.control_points) != len(target.control_points):
                print('Force: source=%d target=%d' % (len(source.control_points), len(target.control_points)))
            while len(source.control_points) < len(target.control_points):
                source.add_one()
            while len(target.control_points) < len(source.control_points):
                target.add_one()
        self.orig = source
        self.morph = source.fixed()
        self.target = target
        self.t_func = t_func
        self.validate()
        count = model.replace(self.orig, self.morph)
        if not count:
            raise MorphError('Cannot find source in model')

    def validate(self):
        if len(self.orig.control_points) != len(self.target.control_points):
            raise MorphError('%s.#cp=%d %s.#cp=%d' % (
                'orig', len(self.orig.control_points),
                'target', len(self.target.control_points)))

    def update(self, t):
        t = self.t_func(t)

        morph_cp = self.morph.control_points
        orig_cp = self.orig.control_points
        target_cp = self.target.control_points

        def pts(cp):
            return cp.c, cp.dl, cp.dr

        if t is None:
            # Hidden hack--just move off screen
            for morph in morph_cp:
                morph.c.setxy(1e6, 1e6)
                morph.dl.setxy(0, 0)
                morph.dr.setxy(0, 0)
            return

        for morph, orig, target in zip(morph_cp, orig_cp, target_cp):
            for m, o, tgt in zip(pts(morph), pts(orig), pts(target)):
                # print(' mot=', m, o, tgt)
                m.setxy(*(o + t * (tgt - o)).xy())

    def restore(self):
        self.model.replace(self.morph, self.orig)


class MorphMultiStep(Animation):
    def __init__(self, model: Group, source: ElemCurve,
                 targets: List[Tuple[float, ElemCurve]], t_func: Callable, force=True):
        super().__init__(Point(0, 0))
        self.model = model
        self.orig = source
        all_steps, all_curves = zip(*([(0.0, source.copy())] + targets))
        self.all_curves: List[ElemCurve] = all_curves
        self.all_steps: List[float] = all_steps
        max_len = max(len(c.control_points) for c in self.all_curves)
        for c in self.all_curves:
            while len(c.control_points) < max_len:
                c.add_one()
            # TODO-make sure points are CCW
            # Rotate the so that lower left is 0
            rotate = force
            if rotate:
                bbox = c.bbox()
                dists = sorted([((bbox.p1-cp.c).length(), idx) for idx, cp in enumerate(c.control_points)])
                ll = dists[0][1]
                old_len = len(c.control_points)
                c.control_points = c.control_points[ll:] + c.control_points[:ll]
                assert old_len == len(c.control_points)

        self.morph = self.all_curves[0].fixed()
        self.t_func = t_func
        count = model.replace(self.orig, self.morph)
        if not count:
            raise MorphError('Cannot find source in model')

    def update(self, t):
        morph_cps = self.morph.control_points

        t = self.t_func(t)
        if t is None:
            # Hidden hack--just move off screen
            for morph_cp in morph_cps:
                morph_cp.c.setxy(1e6, 1e6)
                morph_cp.dl.setxy(0, 0)
                morph_cp.dr.setxy(0, 0)
            return

        idx = bisect.bisect_right(self.all_steps, t)
        if idx == 0:
            low_c = self.all_curves[0]
            high_c = low_c
        elif idx >= len(self.all_curves):
            low_c = self.all_curves[-1]
            high_c = low_c
        else:
            low_c = self.all_curves[idx-1]
            high_c = self.all_curves[idx]
            t = (t-self.all_steps[idx-1]) / (self.all_steps[idx] - self.all_steps[idx-1])

        low_cps = low_c.control_points
        high_cps = high_c.control_points

        def pts(cp):
            return cp.c, cp.dl, cp.dr

        for morph_cp, low_cp, high_cp in zip(morph_cps, low_cps, high_cps):
            for morph_pt, low_pt, high_pt in zip(pts(morph_cp), pts(low_cp), pts(high_cp)):
                # print(' mot=', m, o, tgt)
                morph_pt.setxy(*(low_pt + t * (high_pt - low_pt)).xy())

    def restore(self):
        self.model.replace(self.morph, self.orig)


# noinspection DuplicatedCode
def rgb_to_transparent(im, colors=256, palette_image=None, two_color_flip=False):
    # See: https://stackoverflow.com/questions/46850318/transparent-background-in-gif-using-python-imageio
    assert im.mode == 'RGB'

    if palette_image:
        if sys.platform == 'ios':
            im = im.convert('P', palette=palette_image, dither=Image.NONE, colors=colors - 1)
        else:
            # quantize(self, colors=256, method=None, kmeans=0, palette=None, dither=1):
            im = im.quantize(palette=palette_image, dither=Image.NONE)
    else:
        im = im.convert('P', palette=Image.ADAPTIVE, colors=colors - 1)
        if two_color_flip:
            # A bit of laziness.  Turns out for white images, the ADAPTIVE palette is [almost-white, black],
            # so we can turn it into [black, white] fairly easily.
            im = im.remap_palette([1, 0])  # Rewrite the image with 0 as black and 1 as white
            im.palette.palette = b'\xFF' * 768  # Now, make the palette all white
            im.palette.getcolor((0, 0, 0))  # Except for first entry as black

    im.info['transparency'] = im.getpixel((0, 0))  # Assume upper-left pixel should be transparent

    return im


class Builder(object):
    """Holder for building a modelled image or animation"""

    def __init__(self, base: Image.Image, matrix: Transform, model: Group, animations=None, duration=2.0, draft=True):
        self.base = base
        self.matrix = matrix
        self.model = model
        self.animations = animations or AnimationHolder()
        self.draft = draft
        self.duration = duration
        self.images: List[Image.Image] = []
        self.show_frame = not True

    def build_one(self, t=0, step=0):
        """Build one frame"""
        drawing = DrawingContext(self.base, matrix=self.matrix, prod=not self.draft)
        # drawing.show_cps = True
        self.animations.update(t)
        self.model.draw(drawing)
        if self.show_frame:
            drawing.text(2, 2, 't=%0.4f #%02d' % (t, step))
        return drawing.image()

    def build_all(self, steps):
        self.images = [self.build_one(t / steps, t) for t in range(steps)]
        return self.images

    def max_bbox(self, images=None):
        images = images or self.images
        bb = images[0].getbbox()
        for im in images[1:]:
            bb = bbox_max(bb, im.getbbox())
        print('BBox max: %s %s over %d images' % (images[0].size, bb, len(images)))
        return bb

    @staticmethod
    def resize_for_gif(image: Image.Image, x_size, y_size):
        """
            Resize an RGBA image so that internal areas are down-sampled nicely, but alpha
            is binary.  This is because GIF only has binary alpha.

            Relies on under the following assumptions:
                1. Alpha in source image is either on or off
                2. ?

        """

        # This image looks good, but the borders have blurred alpha and GIF does not support that
        shrunk = image.resize((x_size, y_size), resample=Image.BICUBIC)
        if shrunk.mode == 'RGBA':
            # Fix the alpha channel to be On or Off
            # shrunk.save('/tmp/shrunk.png')
            a = getalpha(shrunk).point(lambda v: 0 if v < 255 else 255)
            shrunk.putalpha(a)
            # shrunk.save('/tmp/shrunk_post_alpha.png')
            debug = False
            if debug:
                shrunk.show()
                composed(shrunk, 'white').show()
                composed(shrunk, 'palegoldenrod').show()
        return shrunk

    def scaled(self, scale, bbox=None, images=None):
        images = images or self.images
        if bbox:
            images = [im.crop(box=bbox) for im in images]
        if scale == 1:
            scaled = images
        else:
            x, y = images[0].size
            x_scaled = x // scale
            y_scaled = y // scale
            scaled = [self.resize_for_gif(im, x_scaled, y_scaled) for im in images]
        return scaled

    @staticmethod
    def make_palette(images):
        """Create a 'P' mode image to use as conversion palette"""

        debug = not True
        # This gives a nice 'P' ramp image for test display
        im = imagehelp.palette_image()
        # Histogram of all colors in image
        colors = {}
        for image in images:
            for color in image.getdata():
                colors.setdefault(color, 0)
                colors[color] += 1
        if debug:
            print('make_palette: found %d colors' % len(colors))
        all_colors = list(reversed(sorted([(v, k) for k, v in colors.items()])))

        im.palette.colors = {}  # Start over on list of colors
        for count, color in all_colors[:256]:
            im.palette.getcolor(color)
        im.load()  # Force palette to be loaded into actual image
        if debug:
            im.show()
        return im

    def save_animation(self, output, images=None, autocrop=True):
        if not output:
            output = TMP_ANIM
            print('Output to %r' % output)
        if not images:
            images = self.images
        if autocrop:
            xs, ys = images[0].size
            bb = self.max_bbox(images)
            xl, yl, xh, yh = bb
            radius = 16
            bb = (max(0, xl - radius), max(0, yl - radius), min(xs, xh + radius), min(ys, yh + radius))
            images = [im.crop(bb) for im in images]
        images = self.scaled(2, images=images)
        ms_per_frame = int(1000 * self.duration / len(images))
        if images[0].mode != 'RGB':
            # RGBA does not work for .gif output
            images = [composed(img, 'black').convert('RGB') for img in images]
        images_rgba = images
        palette = self.make_palette(images_rgba)
        images = [rgb_to_transparent(img, palette_image=palette) for img in images]
        if sys.platform == 'darwin':
            images_rgba[0].save('/tmp/images_rgba.png')
            images[0].save('/tmp/images.png')
            images[0].save(output, save_all=True, append_images=images[1:], disposal=2, duration=ms_per_frame, loop=0)
            import pygifsicle
            pygifsicle.optimize('/tmp/anim.gif', '/tmp/anim_opt.gif')
            platform.quicklook('/tmp/anim_opt.gif')
        elif sys.platform == 'ios':
            # noinspection PyUnresolvedReferences,PyPackageRequirements
            from images2gif import writeGif
            images[0].show()
            writeGif(output, images, duration=ms_per_frame / 1000.0)
            # [im.resize((100,100)).show() for im in images]
            platform.quicklook(output)

    def run(self, steps=10, output=None):
        self.build_all(steps=steps)
        self.save_animation(output)


def run_model(model, animations):
    base_image = Image.new('RGBA', (1000, 1000), 'white')
    matrix = Transform().scale(5, -5).translate(500, 500)
    DrawingContext(base_image, matrix).grid()
    builder = Builder(base_image, matrix, model, animations, draft=True)
    builder.run(40)


def test_morphs():
    animations = AnimationHolder()

    pens = PensByShape().replace_width(0)
    model = GroupBuilder('test', pens, shape_kind='edge_filled')
    a = model.curve('a', shape_kind=PenBrush('black', 'yellow'), cps=[
        ControlPoint(Point(-10, -50), Vector(50, 100), Vector(-50, -100)),
        ControlPoint(Point(50, 50), Vector(-100, 50), Vector(100, -50)),
        ControlPoint(Point(50, -20), Vector(0, -50), Vector(0, 50)),
    ])
    targets = GroupBuilder('test', pens)
    b = targets.curve('b', closed=True, cps=[
        ControlPoint(Point(50, 50), Vector(100, -50), Vector(-100, 50)),
        ControlPoint(Point(50, -20), Vector(0, -50), Vector(0, 50)),
        ControlPoint(Point(-20, -50), Vector(50, 100), Vector(-50, -100)),
    ])
    # c = targets.rect('c', Point(50, 50), Point(-50, -25))

    m = Morph(model.the_group, a, b, Animation.sin(scale=0.5, shift=0.5))
    animations.add(m)
    # animations = AnimationHolder()
    # model.the_group.replace(a, b)
    run_model(model.the_group, animations)


def test_animations():
    anims = AnimationHolder()

    pens = PensByShape().replace_width(5)
    test = GroupBuilder('test', pens)

    wid = 30
    for n in range(4):
        x = wid * n - 45
        a = test.point('t%s_a' % n, x, -60)
        b = test.point('t%s_b' % n, x, 60)
        e = test.curve_old('t%s' % n)
        e.c((a, x + 10, -25, x - 10, 25, b))
        if n == 0:
            anims.add(AnimationLinear(a, Point(x - 10, -50)))
        elif n == 1:
            anims.add(AnimationSinusoidal(a, Point(x - 10, -50), frequency=2.0))
        elif n == 2:
            anims.add(AnimationSinusoidal(a, Point(x - 10, -50)))
        elif n == 3:
            anims.add(AnimationSinusoidal(a, Point(x - 10, -50), offset=90))

    run_model(test, anims)


def test_images():
    image = Image.open('/tmp/full_snap_alpha.png')
    # image.show()
    x, y = image.size
    scale = 5
    x, y = x // scale, y // scale
    Builder.resize_for_gif(image, x, y)


def test_anim_funcs():
    # noinspection PyListCreation
    funcs = []

    funcs.append(('ramp_up', Animation.ramp_up()))
    funcs.append(('ramp_down', Animation.ramp_down()))

    do_extras = False
    if do_extras:
        funcs.append(('identity', Animation.identity()))
        xy_test = Animation.xy(Animation.ramp_up(start=0.1, end=0.9), Animation.ramp_up(start=0.2, end=0.3))
        funcs.append(('xy_test', xy_test))

        def halfish(t):
            x, y = xy_test(t)
            return x / 2 + 0.25, y / 2 + 0.25

        funcs.append(('halfish', halfish))

    if do_extras:
        funcs.append(('interp1', Animation.interpolate([(0, 0), (0.5, 1), (1, 0)])))
        funcs.append(('interp2', Animation.interpolate([(0, 0), (0.25, 1), (0.75, 1), (1, 0)])))
        funcs.append(('interp3', Animation.interpolate([(0, -0.5), (0.1, 1), (0.8, 0), (0.9, 0), (1, -0.5)])))

        funcs.append(('sin', Animation.sin()))
        funcs.append(('cos', Animation.cos(frequency=2)))
        funcs.append(('sin_cos', Animation.sin_cos(scale=0.5, shift=2.0)))
    Animation.plot(funcs)


def test_all():
    # test_images()
    test_animations()


if __name__ == '__main__':
    # test_animations()
    # test_all()
    # test_anim_funcs()
    test_morphs()
