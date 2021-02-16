"""
add glsl renderers/shaders to your kivy widget
==============================================

This ae namespace portion provides the mixin class :class:`ShadersMixin` that can be combined with
any Kivy widget/layout for to display GLSL-/shader-based graphics, gradients and animations.

Additionally some :ref:`built-in shaders` are integrated into this portion. More shader examples can be found in
the glsl sub-folder of the `GlslTester <https://github.com/AndiEcker/glsl_tester>`_ demo application.


usage of ShadersMixin class
---------------------------

For to add the :class:`ShadersMixin` mixin class to a Kivy widget in your python code file you have to
specify it in the declaration of your widget class. The following example is extending Kivy's
:class:`~kivy.uix.boxlayout.BoxLayout` layout with a shader::

    from kivy.uix.boxlayout import BoxLayout
    from ae.kivy_glsl import ShadersMixin

    class MyBoxLayoutWithShader(ShadersMixin, BoxLayout):


Alternatively you can declare a your shader-widget as a new kv rule within a kv file::

    <MyBoxLayoutWithShader@ShadersMixin+BoxLayout>


For to activate a shader call the :meth:`ShadersMixin.add_renderer` method::

    renderer_index = widget_instance.add_renderer()


By default :meth:`~ShadersMixin.add_renderer` is using the built-in
:data:`plasma hearts shader <PLASMA_HEARTS_SHADER_CODE>`, provided by this portion. The next example is instead using
the built-in :data:`touch wave shader <TOUCH_WAVE_SHADER_CODE>`::

    from ae.kivy_glsl import BUILT_IN_SHADERS

    widget_instance.add_renderer(shader_code=BUILT_IN_SHADERS['touch_wave'])


Alternatively you can use your own shader code by specifying it on call of the method :meth:`~ShadersMixin.add_renderer`
either as code block string to the `paramref:`~ShadersMixin.add_renderer.shader_code` argument or as file name to the
`paramref:`~ShadersMixin.add_renderer.shader_file` argument.

Animation shaders like the built-in touch wave and plasma hearts shaders need to be refreshed by a timer.
The refreshing frequency can be specified via the :paramref:`~ShadersMixin.add_renderer.update_freq` parameter.
For to disable the automatic creation of a timer event pass a zero value to this argument.

.. hint::
    The demo apps `ComPartY <https://gitlab.com/ae-group/comparty>`_ and
    `GlslTester <https://github.com/AndiEcker/glsl_tester>`_ are disabling the automatic timer event
    for each shader and using instead a Kivy clock timer for to update the frames of all active shaders.


Store the return value of :meth:`~ShadersMixin.add_renderer` renderer_index if you later want to deactivate the shader
with the :meth:`~ShadersMixin.del_renderer` method::

    widget_instance.del_renderer(renderer_index)


.. note::
    You can activate multiple shaders for the same widget. The visibility and intensity of each shader depends then on
    the implementation of the shader codes and the values of the input arguments (especially `alpha` and `tex_col_mix`)
    for each shader (see parameter :paramref:`~ShadersMixin.add_renderer.glsl_dyn_args`).


shader compilation errors and renderer crashes
----------------------------------------------

On some devices (mostly on Android) the shader script does not compile. The success property of Kivy's shader class
is then set to False and an error message like the following gets printed on to the console output::

    [ERROR  ] [Shader      ] <fragment> failed to compile (gl:0)
    [INFO   ] [Shader      ] fragment shader: <b"0:27(6): error: ....

Some common failure reasons are:

* missing declaration of used uniform input variables.
* non-input/output variables declared on module level (they should be moved into main or any other function).

In other cases the shader code compiles fine but then the renderer is crashing in the vbo.so library and w/o
printing any Python traceback to the console - see also `this Kivy issues <https://github.com/kivy/kivy/issues/6627>`_).

Sometimes this crashes can be prevented if the texture of the widget (or of the last shader) gets fetched
(w/ the function texture2D(texture0, tex_coord0)) - even if it is not used for the final gl_FragColor output variable.

In some cases additional to fetch the texture, the return value of the `texture2D` call has to be accessed at least once
at the first render cycle.


built-in shaders
----------------

The :data:`circled alpha shader <CIRCLED_ALPHA_SHADER_CODE>` is a simple gradient pixel shader without any time-based
animations.

The :data:`touch wave shader <TOUCH_WAVE_SHADER_CODE>` is animated and inspired by the kivy pulse shader example
(Danguafer/Silexars, 2010) https://github.com/kivy/kivy/blob/master/examples/shader/shadertree.py.

The animated :data:`plasma hearts shader <PLASMA_HEARTS_SHADER_CODE>` is inspired by the kivy plasma shader example
https://github.com/kivy/kivy/blob/master/examples/shader/plasma.py.

.. hint::
    The `GlslTester <https://github.com/AndiEcker/glsl_tester>`_ and `ComPartY <https://gitlab.com/ae-group/comparty>`_
    applications are demonstrating the usage of this portion.

The literals of the built-in shaders got converted into constants, following the recommendations given in the accepted
answer of `this SO question <https://stackoverflow.com/questions/20936086>`_.
"""
from functools import partial
from typing import Any, Dict, Iterable, List, Optional

from kivy.clock import Clock                                    # type: ignore
from kivy.factory import Factory                                # type: ignore
from kivy.graphics.instructions import Canvas, RenderContext    # type: ignore # pylint: disable=no-name-in-module
from kivy.graphics.vertex_instructions import Rectangle         # type: ignore # pylint: disable=no-name-in-module

from ae.base import UNSET                                       # type: ignore


__version__ = '0.1.4'


RendererType = Dict[str, Any]       #: used for to store renderer

# --- BUILT-IN SHADERS

CIRCLED_ALPHA_SHADER_CODE = '''\
$HEADER$

uniform float alpha;
uniform float tex_col_mix;
uniform vec2 center_pos;
uniform vec2 pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

void main(void)
{
  vec2 pix_pos = (frag_modelview_mat * gl_FragCoord).xy - pos;
  float len = length(pix_pos - center_pos);
  float dis = len / max(pix_pos.x, max(pix_pos.y, max(resolution.x - pix_pos.x, resolution.y - pix_pos.y)));
  vec3 col = tint_ink.rgb;
  if (tex_col_mix != 0.0) {
    vec4 tex = texture2D(texture0, tex_coord0);
    col = mix(tex.rgb, col, tex_col_mix);
  }
  gl_FragColor = vec4(col, dis * alpha);
}
'''

PLASMA_HEARTS_SHADER_CODE = '''\
$HEADER$

uniform float alpha;
uniform float contrast;
uniform float tex_col_mix;
uniform float time;
uniform vec2 center_pos;
uniform vec2 pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

const float THOUSAND = 963.9;
const float HUNDRED = 69.3;
const float TEN = 9.9;
const float TWO = 1.83;
const float ONE = 0.99;

void main(void)
{
  vec2 pix_pos = (frag_modelview_mat * gl_FragCoord).xy - pos;
  float x = abs(pix_pos.x - center_pos.x);
  float y = abs(pix_pos.y - center_pos.y - resolution.y);

  float m1 = x + y + cos(sin(time) * TWO) * HUNDRED + sin(x / HUNDRED) * THOUSAND;
  float m2 = y / resolution.y;
  float m3 = x / resolution.x + time * TWO;

  float c1 = abs(sin(m2 + time) / TWO + cos(m3 / TWO - m2 - m3 + time));
  float c2 = abs(sin(c1 + sin(m1 / THOUSAND + time) + sin(y / HUNDRED + time) + sin((x + y) / HUNDRED) * TWO));
  float c3 = abs(sin(c2 + cos(m2 + m3 + c2) + cos(m3) + sin(x / THOUSAND)));

  vec4 tex = texture2D(texture0, tex_coord0);
  float dis = TWO * distance(pix_pos, center_pos) / min(resolution.x, resolution.y);
  vec4 col = vec4(c1, c2, c3, contrast * (ONE - dis)) * tint_ink * TWO;
  col = mix(tex, col, tex_col_mix);
  gl_FragColor = vec4(col.rgb, col.a * sqrt(alpha));
}
'''

COLORED_SMOKE_SHADER_CODE = '''\
$HEADER$

uniform float alpha;
uniform float contrast;
uniform float tex_col_mix;
uniform float time;
uniform vec2 center_pos;
uniform vec2 mouse;         // density, speed
uniform vec2 pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

const float ONE = 0.99999999999999;

float rand(vec2 n) {
 //This is just a compounded expression to simulate a random number based on a seed given as n
 return fract(cos(dot(n, vec2(12.98982, 4.14141))) * 43758.54531);
}

float noise(vec2 n) {
 //Uses the rand function to generate noise
 const vec2 d = vec2(0.0, ONE);
 vec2 b = floor(n), f = smoothstep(vec2(0.0), vec2(ONE), fract(n));
 return mix(mix(rand(b), rand(b + d.yx), f.x), mix(rand(b + d.xy), rand(b + d.yy), f.x), f.y);
}

float fbm(vec2 n) {
 //fbm stands for "Fractal Brownian Motion" https://en.wikipedia.org/wiki/Fractional_Brownian_motion
 float total = 0.0;
 float amplitude = 1.62;
 for (int i = 0; i < 3; i++) {
  total += noise(n) * amplitude;
  n += n;
  amplitude *= 0.51;
 }
 return total;
}

void main() {
 //This is where our shader comes together
 const vec3 c1 = vec3(126.0/255.0, 0.0/255.0, 96.9/255.0);
 //const vec3 c2 = vec3(173.0/255.0, 0.0/255.0, 161.4/255.0);
 vec3 c2 = tint_ink.rgb;
 const vec3 c3 = vec3(0.21, 0.0, 0.0);
 const vec3 c4 = vec3(165.0/255.0, 129.0/255.0, 214.4/255.0);
 const vec3 c5 = vec3(0.12);
 const vec3 c6 = vec3(0.9);
 vec2 pix_pos = (gl_FragCoord.xy - pos - center_pos) / resolution.xy - vec2(0.0, 0.51);
 //This is how "packed" the smoke is in our area. Try changing 15.0 to 2.1, or something else
 vec2 p = pix_pos * (ONE + mouse.x / resolution.x * 15.0);
 //The fbm function takes p as its seed (so each pixel looks different) and time (so it shifts over time)
 float q = fbm(p - time * 0.12);
 float speed = 3.9 * time * mouse.y / resolution.y;
 vec2 r = vec2(fbm(p + q + speed - p.x - p.y), fbm(p + q - speed));
 vec3 col = (mix(c1, c2, fbm(p + r)) + mix(c3, c4, r.y) - mix(c5, c6, r.x)) * cos(contrast * pix_pos.y);
 col *= ONE - pix_pos.y;
 if (tex_col_mix != 0.0) {
  vec4 tex = texture2D(texture0, tex_coord0);
  col = mix(tex.rgb, col, tex_col_mix);
 }
 gl_FragColor = vec4(col, (alpha + tint_ink.a) / 2.01);
}
'''

FIRE_STORM_SHADER_CODE = '''\
$HEADER$

uniform float alpha;
uniform float contrast;  // speed
uniform float tex_col_mix;
uniform float time;
uniform vec2 center_pos;
uniform vec2 mouse;  // intensity, granularity
uniform vec2 pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

#define TAU 6.283185307182
#define MAX_ITER 15

void main( void ) {
 float t = time*contrast + 23.01;
 // uv should be the 0-1 uv of texture...
 vec2 xy = (gl_FragCoord.xy - pos - center_pos) / resolution.yy; // - vec2(0.9);
 vec2 uv = vec2(atan(xy.y, xy.x) * 6.99999 / TAU, log(length(xy)) * (0.21 + mouse.y / resolution.y) - time * 0.21);
 vec2 p = mod(uv*TAU, TAU)-250.02;
 vec2 i = vec2(p);
 float c = 8.52;
 float intensity = 0.0015 + mouse.x / resolution.x / 333.3;  // = .005;

 for (int n = 0; n < MAX_ITER; n++) {
   float t = t * (1.02 - (3.498 / float(n+1)));
   i = p + vec2(cos(t - i.x) + sin(t + i.y), sin(t - i.y) + cos(t + i.x));
   c += 1.0/length(vec2(p.x / (sin(i.x+t)/intensity),p.y / (cos(i.y+t)/intensity)));
 }
 c /= float(MAX_ITER);
 c = 1.272 - pow(c, 6.42);
 vec3 colour = vec3(pow(abs(c), 8.01));
 colour = clamp(colour + tint_ink.rgb, 0.0, 0.999999);
 if (tex_col_mix != 0.0) {
  vec4 tex = texture2D(texture0, tex_coord0);
  colour = mix(tex.rgb, colour, tex_col_mix);
 }
 gl_FragColor = vec4(colour, (alpha + tint_ink.a) / 2.00001);
 }
'''

TOUCH_WAVE_SHADER_CODE = '''\
$HEADER$

uniform float alpha;
uniform float contrast;
uniform float tex_col_mix;
uniform float time;
uniform vec2 center_pos;
uniform vec2 pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

const float TEN = 9.99999;
const float TWO = 2.00001;
const float ONE = 0.99999;

void main(void)
{
  vec2 pix_pos = (frag_modelview_mat * gl_FragCoord).xy - pos;
  float len = length(pix_pos - center_pos);
  float col_comp = (sin(len / TEN - time * TEN) + ONE) / TEN;
  float dis = len / (TWO * max(resolution.x, resolution.y));
  vec4 col = tint_ink / vec4(col_comp, col_comp, col_comp, dis / (ONE / TEN + contrast)) / TEN;
  if (tex_col_mix != 0.0) {
    vec4 tex = texture2D(texture0, tex_coord0);
    col = mix(tex, col, tex_col_mix);
  }
  gl_FragColor = vec4(col.rgb, col.a * alpha * alpha);
}
'''

WORM_WHOLE_SHADER_CODE = '''\
$HEADER$

uniform float alpha;
uniform float contrast;
uniform float tex_col_mix;
uniform float time;
uniform vec2 center_pos;
uniform vec2 mouse;         // off1, off2
uniform vec2 pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

const float ONE = 0.99999999999;
const float TWO = 1.99999999998;

void main(void){
 vec2 centered_coord = (TWO * (gl_FragCoord.xy - pos - center_pos) - resolution) / resolution.y;
 centered_coord += vec2(resolution.x / resolution.y, ONE);
 centered_coord.y *= dot(centered_coord,centered_coord);
 float dist_from_center = length(centered_coord);
 float dist_from_center_y = length(centered_coord.y);
 float u = 6.0/dist_from_center_y + time * 3.999;
 float v = (10.2/dist_from_center_y) * centered_coord.x;
 float grid = (ONE-pow(sin(u)+ONE, 0.6) + (ONE-pow(sin(v)+ONE, 0.6)))*dist_from_center_y*30.0*(0.03+contrast);
 float off1 = sin(fract(time*0.48)*6.27+dist_from_center*5.0001)*mouse.x/resolution.x;
 float off2 = sin(fract(time*0.48)*6.27+dist_from_center_y*12.0)*mouse.y/resolution.y;
 vec3 col = vec3(grid) * vec3(tint_ink.r*off1,tint_ink.g,tint_ink.b*off2);
 if (tex_col_mix != 0.0) {
  vec4 tex = texture2D(texture0, tex_coord0);
  col = mix(tex.rgb, col, tex_col_mix);
 }
 gl_FragColor=vec4(col, alpha);
}
'''

BUILT_IN_SHADERS = dict(
    circled_alpha=CIRCLED_ALPHA_SHADER_CODE, colored_smoke=COLORED_SMOKE_SHADER_CODE, fire_storm=FIRE_STORM_SHADER_CODE,
    plasma_hearts=PLASMA_HEARTS_SHADER_CODE, touch_wave=TOUCH_WAVE_SHADER_CODE, worm_whole=WORM_WHOLE_SHADER_CODE)
""" dict of built-in shader codes. """


class ShadersMixin:
    """ shader mixin base class """
    # abstract attributes provided by the Widget instance mixed into
    canvas: Any
    center_x: float
    center_y: float
    pos: list
    size: list

    # attributes
    renderers: List[RendererType] = list()  #: list/pool of active shaders/render-contexts

    def add_renderer(self, add_to: Optional[Canvas] = None,
                     shader_code: str = PLASMA_HEARTS_SHADER_CODE, shader_file: str = "",
                     start_time: Optional[float] = 0.0, update_freq: float = 30.0,
                     **glsl_dyn_args) -> int:
        """ create new render context canvas and add it.

        :param add_to:          canvas or existing render context to add the new render context to. If not passed then
                                the canvas of the widget instance mixed-into will be used if exists. If the
                                canvas does not exist then the new render context will be set as a normal canvas.
                                By passing an already existing render context (e.g. self.renderers[-1]['render_ctx'])
                                then the new render context will be added to the passed one - in this case the new
                                render context will also get invisible if you delete the passed render context.
        :param shader_code:     fragment shader code block (will be ignored if :paramref:`.shader_file` is not empty).
        :param shader_file:     filename with the glsl shader code (with “–VERTEX” or “–FRAGMENT” sections) to load.
        :param start_time:      base/start time. Passing the default value zero is syncing the `time` glsl parameter
                                of this renderer with :meth:`kivy.clock.Clock.get_boottime()`.
                                Pass None for to initialize this argument to the current Clock boot time; this
                                way the `time` glsl argument will start by zero.
        :param update_freq:     shader/renderer update frequency. Pass 0.0 for to disable creation of an update timer.
        :param glsl_dyn_args:   extra/user dynamic shader parameters, depending on the used shader code. The keys
                                of this dict are the names of the corresponding glsl input variables in your shader
                                code. The built-in shaders (provided by this module) providing the following glsl
                                input variables:

                                * `'alpha'`: opacity (float, 0.0 - 1.0).
                                * `'center_pos'`: center position in Window coordinates (tuple(float, float)).
                                * `'contrast'`: color contrast (float, 0.0 - 1.0).
                                * `'mouse'`: mouse pointer position in Window coordinates (tuple(float, float)).
                                * `'resolution'`: width and height in Window coordinates (tuple(float, float)).
                                * `'tex_col_mix'`: factor (float, 0.0 - 1.0) for to mix the kivy input texture
                                   and the calculated color. A value of 1.0 will only show the shader color,
                                   whereas 0.0 will result in the color of the input texture (uniform texture0).
                                * `'tint_ink'`: tint color with color parts in the range 0.0 till 1.0.
                                * `'time'`: animation time (offset to :paramref:`.start_time`) in seconds. If
                                   specified as constant (non-dynamic) value then you have to call the
                                   :meth:`.next_tick` method for to increment the timer for this shader/renderer.

                                Pass a callable for to provide a dynamic/current value, which will be called on
                                each rendering frame without arguments and the return value will be passed into
                                the glsl shader.

                                .. note::
                                    Don't pass `int` values because some renderer will interpret them as `0.0`.

        :return:                index (id) of the created/added render context.
        """
        # ensure window render context
        # noinspection PyUnresolvedReferences
        import kivy.core.window     # type: ignore # noqa: F401 # pylint: disable=unused-import, import-outside-toplevel

        if start_time is None:
            start_time = Clock.get_boottime()
        if 'center_pos' not in glsl_dyn_args:
            glsl_dyn_args['center_pos'] = lambda: (self.center_x, self.center_y)
        if 'tint_ink' not in glsl_dyn_args:
            glsl_dyn_args['tint_ink'] = (0.546, 0.546, 0.546, 1.0)    # colors * shader_code.TWO ~= (1.0, 1.0, 1.0)

        ren_ctx = RenderContext(use_parent_modelview=True, use_parent_projection=True, use_parent_frag_modelview=True)
        with ren_ctx:
            rectangle = Rectangle(pos=self.pos, size=self.size)

        shader = ren_ctx.shader
        try:
            if shader_file:
                old_value = shader.source
                shader.source = shader_file
            else:
                old_value = shader.fs
                shader.fs = shader_code
            fail_reason = "" if shader.success else "shader.success is False"
        except Exception as ex:
            fail_reason = f"exception {ex}"
            old_value = UNSET
        if fail_reason:
            if old_value is not UNSET:
                if shader_file:
                    shader.source = old_value
                else:
                    shader.fs = old_value
            raise ValueError(f"ShadersMixin.add_renderer: shader compilation failed:{fail_reason} (see console output)")

        renderer_idx = len(self.renderers)
        if renderer_idx == 0:
            self.renderers = list()     # create attribute on this instance (leave class attribute untouched emtpy list)

        if add_to is None and self.canvas is not None:
            add_to = self.canvas
        if add_to is None:
            self.canvas = ren_ctx
        else:
            add_to.add(ren_ctx)

        renderer = dict(added_to=add_to, deleted=False, render_ctx=ren_ctx, rectangle=rectangle,
                        shader_code=shader_code, shader_file=shader_file,
                        start_time=start_time, update_freq=update_freq, glsl_dyn_args=glsl_dyn_args)
        self.renderers.append(renderer)

        if update_freq:
            renderer['timer'] = Clock.schedule_interval(partial(self._refresh_glsl, renderer_idx), 1 / update_freq)

        return renderer_idx

    def del_renderer(self, renderer_idx: int):
        """ remove renderer added via add_renderer.

        :param renderer_idx:    index of the renderer to remove (returned by :meth:`.add_renderer`). If the passed
                                index value is less then zero then :attr:`~ShadersMixin.renderers` left untouched.
        """
        if renderer_idx < 0 or not self.renderers or renderer_idx >= len(self.renderers):
            return              # ignore if app disabled rendering for too slow devices or on duplicate render deletion

        renderer = self.renderers[renderer_idx]
        renderer['deleted'] = True
        self.reset_timers(remove_deleted=True)
        if renderer_idx == len(self.renderers) - 1:
            renderer = self.renderers.pop(renderer_idx)
            while self.renderers and self.renderers[-1]['deleted']:
                self.renderers.pop(-1)

        added_to = renderer['added_to']
        if added_to:
            added_to.remove(renderer['render_ctx'])
        else:
            self.canvas = None

    def next_tick(self, increment: float = 1 / 30.):
        """ increment glsl `time` input argument if renderers get updated manually/explicitly by the app.

        :param increment:       delta in seconds for the next refresh of all renderers with a `time` constant.
        """
        for renderer in self.renderers:
            if not renderer['deleted']:
                dyn_args = renderer['glsl_dyn_args']
                if 'time' in dyn_args and not callable(dyn_args['time']):
                    dyn_args['time'] += increment

    def on_pos(self, _instance: Any, value: Iterable):
        """ pos """
        for ren in self.renderers:
            if not ren['deleted']:
                ren['rectangle'].pos = value

    def on_size(self, _instance: Any, value: Iterable):
        """ size changed """
        for ren in self.renderers:
            if not ren['deleted']:
                ren['rectangle'].size = value

    def _refresh_glsl(self, renderer_idx: int, _dt: float):
        """ timer/clock event handler for to animate and sync one canvas shader. """
        self.refresh_renderer(self.renderers[renderer_idx])

    def refresh_renderer(self, renderer: RendererType):
        """ update the shader arguments for the current animation frame.

        :param renderer:        dict with render context, rectangle and glsl input arguments.
        """
        ren_ctx = renderer['render_ctx']
        start_time = renderer['start_time']
        if callable(start_time):
            start_time = start_time()

        # first set the defaults for glsl fragment shader input args (uniforms)
        glsl_kwargs = renderer['glsl_dyn_args']
        ren_ctx['alpha'] = 0.99
        ren_ctx['contrast'] = 0.69
        ren_ctx['pos'] = list(map(float, self.pos))
        ren_ctx['resolution'] = list(map(float, self.size))
        ren_ctx['tex_col_mix'] = 0.69
        if not callable(glsl_kwargs.get('time')):
            ren_ctx['time'] = Clock.get_boottime() - start_time

        # .. then overwrite glsl arguments with dynamic user values
        for key, val in glsl_kwargs.items():
            ren_ctx[key] = val() if callable(val) else val

    def refresh_renderers(self):
        """ manually update all renderers. """
        for renderer in self.renderers:
            self.refresh_renderer(renderer)

    def reset_timers(self, remove_deleted: bool = False):
        """ unschedule (if created) and reschedule (if only_remove_deleted=False) active timers of this instance.

        :param remove_deleted:  pass True to only remove deleted times (all active shaders will keep their old timer).
        """
        for idx, renderer in enumerate(self.renderers):
            update_freq = renderer['update_freq']
            deleted = renderer['deleted']
            if update_freq and 'timer' in renderer and (deleted or not remove_deleted):
                Clock.unschedule(renderer['timer'])
                if not deleted:
                    renderer['timer'] = Clock.schedule_interval(partial(self._refresh_glsl, idx), 1 / update_freq)


Factory.register('ShadersMixin', cls=ShadersMixin)
