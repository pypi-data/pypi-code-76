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

    class MyBoxLayoutWithShader(BoxLayout, ShadersMixin):


Alternatively you can declare a your shader-widget as a new kv rule within a kv file::

    <MyBoxLayoutWithShader@BoxLayout+ShadersMixin>


For to register a shader, call the :meth:`ShadersMixin.add_shader` method::

    shader_id = widget_instance.add_shader()


By default :meth:`~ShadersMixin.add_shader` is using the built-in
:data:`plasma hearts shader <PLASMA_HEARTS_SHADER_CODE>`, provided by this portion. The next example is instead using
the built-in :data:`plunge waves shader <PLUNGE_WAVES_SHADER_CODE>`::

    from ae.kivy_glsl import BUILT_IN_SHADERS

    widget_instance.add_shader(shader_code=BUILT_IN_SHADERS['plunge_waves'])


Alternatively you can use your own shader code by specifying it on call of the method :meth:`~ShadersMixin.add_shader`
either as code block string to the `paramref:`~ShadersMixin.add_shader.shader_code` argument or as file name to the
`paramref:`~ShadersMixin.add_shader.shader_file` argument.

Animation shaders like the built-in plunge waves and plasma hearts shaders need to be refreshed by a timer.
The refreshing frequency can be specified via the :paramref:`~ShadersMixin.add_shader.update_freq` parameter.
For to disable the automatic creation of a timer event pass a zero value to this argument.

.. hint::
    The demo apps `ComPartY <https://gitlab.com/ae-group/comparty>`_ and
    `GlslTester <https://github.com/AndiEcker/glsl_tester>`_ are disabling the automatic timer event
    for each shader and using instead a Kivy clock timer for to update the frames of all active shaders.


Store the return value of :meth:`~ShadersMixin.add_shader` to stop, pause or to delete the shader later. The following
examples demonstrates the deletion of a shader by calling the :meth:`~ShadersMixin.del_shader` method::

    widget_instance.del_shader(shader_id)


.. note::
    You can activate multiple shaders for the same widget. The visibility and intensity of each shader depends then on
    the implementation of the shader codes and the values of the input arguments (especially `alpha` and `tex_col_mix`)
    for each shader (see parameter :paramref:`~ShadersMixin.add_shader.glsl_dyn_args`).


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

The :data:`plunge waves shader <PLUNGE_WAVES_SHADER_CODE>` is animated and inspired by the kivy pulse shader example
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
from typing import Any, Callable, Dict, List, Optional

from kivy.clock import Clock                                    # type: ignore
from kivy.factory import Factory                                # type: ignore
from kivy.graphics.instructions import RenderContext            # type: ignore # pylint: disable=no-name-in-module
from kivy.graphics.vertex_instructions import Rectangle         # type: ignore # pylint: disable=no-name-in-module
from kivy.properties import ListProperty                        # type: ignore
from ae.base import UNSET                                       # type: ignore


__version__ = '0.1.5'


ShaderIdType = Dict[str, Any]                                   #: shader internal data and id

# --- BUILT-IN SHADERS

CIRCLED_ALPHA_SHADER_CODE = '''\
$HEADER$

uniform float alpha;
uniform float tex_col_mix;
uniform vec2 center_pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

void main(void)
{
  vec2 pix_pos = (frag_modelview_mat * gl_FragCoord).xy;
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

PLUNGE_WAVES_SHADER_CODE = '''\
$HEADER$

uniform float alpha;
uniform float contrast;
uniform float tex_col_mix;
uniform float time;
uniform vec2 center_pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

const float TEN = 9.99999;
const float TWO = 2.00001;
const float ONE = 0.99999;

void main(void)
{
  vec2 pix_pos = (frag_modelview_mat * gl_FragCoord).xy;
  float len = length(pix_pos - center_pos);
  float col_comp = (sin(len / TEN - time * TEN) + ONE) / TEN;
  float dis = len / (TWO * min(resolution.x, resolution.y));
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
    plasma_hearts=PLASMA_HEARTS_SHADER_CODE, plunge_waves=PLUNGE_WAVES_SHADER_CODE, worm_whole=WORM_WHOLE_SHADER_CODE)
""" dict of built-in shader codes. """


class ShadersMixin:
    """ shader mixin base class """
    # abstract attributes provided by the Widget instance mixed into
    canvas: Any
    center_x: float
    center_y: float
    dpo: Callable
    fbind: Callable
    parent: Any
    pos: list
    size: list
    to_window: Callable
    unbind_uid: Callable

    # attributes
    started_shaders: List[ShaderIdType] = list()    #: list/pool of active shaders/render-contexts
    added_shaders = ListProperty()                  #: list of kwarg dicts for each shader/renderer

    _pos_fbind_uid: int = 0
    _size_fbind_uid: int = 0

    def on_added_shaders(self, *_args):
        """ added_shaders list property changed event handler. """
        self._update_shaders()

    def on_parent(self, *_args):
        """ parent changed event handler. """
        self._update_shaders()

    def _update_shaders(self):
        shaders_active = self.added_shaders and self.parent

        for shader in reversed(self.started_shaders):
            self.stop_shader(shader, stop=False)

        bound = self._pos_fbind_uid
        if shaders_active:
            for kwargs in self.added_shaders:
                if kwargs['mode'] != 'stop':
                    kwargs['play_error'] = self.play_shader(kwargs)
            if not bound:
                self._pos_fbind_uid = self.fbind('pos', self._pos_changed)  # STRANGE: on_ event not bind-able -> ret==0
                self._size_fbind_uid = self.fbind('size', self._size_changed)
                self._pos_changed()
                self._size_changed()

        elif bound:
            self.unbind_uid('pos', self._pos_fbind_uid)
            self.unbind_uid('size', self._size_fbind_uid)
            self._pos_fbind_uid = 0
            self._size_fbind_uid = 0

    def add_shader(self, add_to: str = '', mode: str = 'play',
                   shader_code: str = PLASMA_HEARTS_SHADER_CODE, shader_file: str = "",
                   start_time: Optional[float] = 0.0, update_freq: float = 30.0,
                   **glsl_dyn_args) -> ShaderIdType:
        """ create new render context canvas and add it.

        :param add_to:          '' to add to current canvas, 'before' and 'after' to the before/after canvas of
                                the widget instance mixed-into. If the canvas does not exist then the shaders
                                render context will be set as a current canvas.
        :param mode:            shader mode, either 'play', 'stop' or 'pause'.
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
        if start_time is None:
            start_time = Clock.get_boottime()
        if 'center_pos' not in glsl_dyn_args:
            glsl_dyn_args['center_pos'] = lambda: (self.center_x, self.center_y)
        if 'tint_ink' not in glsl_dyn_args:
            glsl_dyn_args['tint_ink'] = (0.546, 0.546, 0.546, 1.0)    # colors * shader_code.TWO ~= (1.0, 1.0, 1.0)

        shader_id = dict(add_to=add_to, mode=mode, shader_code=shader_code, shader_file=shader_file,
                         start_time=start_time, update_freq=update_freq, glsl_dyn_args=glsl_dyn_args)

        self.added_shaders.append(shader_id)

        return shader_id

    def del_shader(self, shader_id: ShaderIdType):
        """ remove shader_id added via add_shader.

        :param shader_id:       id of the shader to remove (returned by :meth:`.add_shader`). Ignoring if the passed
                                shader got already removed.
        """
        shaders = self.added_shaders
        if shader_id in shaders[:]:
            self.stop_shader(shader_id)
            shaders.remove(shader_id)

    def next_tick(self, increment: float = 1 / 30.):
        """ increment glsl `time` input argument if started_shaders get updated manually/explicitly by the app.

        :param increment:       delta in seconds for the next refresh of all started_shaders with a `time` constant.
        """
        for shader_id in self.started_shaders:
            dyn_args = shader_id['glsl_dyn_args']
            if 'time' in dyn_args and not callable(dyn_args['time']):
                dyn_args['time'] += increment

    def play_shader(self, shader_id: ShaderIdType) -> str:
        """ create new render context canvas and add it to the widget canvas to display shader output.

        :param shader_id:       shader id.
        :return:                "" if shader is running/playing or error message string.
        """
        # ensure window render context
        # noinspection PyUnresolvedReferences
        import kivy.core.window     # type: ignore # noqa: F401 # pylint: disable=unused-import, import-outside-toplevel

        add_to = shader_id['add_to']
        shader_code = shader_id['shader_code']
        shader_file = shader_id['shader_file']
        update_freq = shader_id['update_freq']
        try:
            ren_ctx = RenderContext(use_parent_modelview=True, use_parent_projection=True,
                                    use_parent_frag_modelview=True)
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
                raise ValueError(f"compilation failed:{fail_reason} (see console output)")

            added_to = self.canvas
            if not added_to:
                self.canvas = ren_ctx
            else:
                if add_to:
                    added_to = added_to.before if add_to == 'before' else added_to.after
                added_to.add(ren_ctx)

            shader_id.update(added_to=added_to, render_ctx=ren_ctx, rectangle=rectangle)
            if not self.started_shaders:
                self.started_shaders = list()  # create attribute on this instance (class attr untouched as emtpy list)
            self.started_shaders.append(shader_id)

            if update_freq:
                shader_id['timer'] = Clock.schedule_interval(partial(self._refresh_glsl, shader_id), 1 / update_freq)

        except (ValueError, Exception) as ex:
            return f"ShadersMixin.add_shader_id: shader start error - {ex}"

        if shader_id['mode'] == 'stop':
            shader_id['mode'] = 'play'

        return ""

    def _pos_changed(self, *_args):
        """ pos changed event handler. """
        for ren in self.started_shaders:
            ren['rectangle'].pos = self.to_window(*self.pos)

    def _size_changed(self, *_args):
        """ size changed event handler. """
        for ren in self.started_shaders:
            ren['rectangle'].size = self.size

    def _refresh_glsl(self, shader_id: ShaderIdType, _dt: float):
        """ timer/clock event handler for to animate and sync one canvas shader. """
        self.refresh_shader(shader_id)

    def refresh_shader(self, shader_id: ShaderIdType):
        """ update the shader arguments for the current animation frame.

        :param shader_id:       dict with render context, rectangle and glsl input arguments.
        """
        ren_ctx = shader_id['render_ctx']
        start_time = shader_id['start_time']
        if callable(start_time):
            start_time = start_time()

        # first set the defaults for glsl fragment shader input args (uniforms)
        glsl_kwargs = shader_id['glsl_dyn_args']
        ren_ctx['alpha'] = 0.99
        ren_ctx['contrast'] = 0.69
        ren_ctx['pos'] = list(map(float, self.to_window(*self.pos)))
        ren_ctx['resolution'] = list(map(float, self.size))
        ren_ctx['tex_col_mix'] = 0.69
        if not callable(glsl_kwargs.get('time')):
            ren_ctx['time'] = Clock.get_boottime() - start_time

        # .. then overwrite glsl arguments with dynamic user values
        for key, val in glsl_kwargs.items():
            ren_ctx[key] = val() if callable(val) else val

    def refresh_started_shaders(self):
        """ manually update all started_shaders. """
        for shader_id in self.started_shaders:
            self.refresh_shader(shader_id)

    def stop_shader(self, shader_id: ShaderIdType, stop: bool = True):
        """ stop shader by removing it from started shaders.

        :param shader_id:       id of the shader to stop. Ignoring if the passed shader got already stopped.
        :param stop:            pass False to prevent that the `mode` of the :paramref:`.shader_id` gets changed
                                'stop' (for internal use to refresh all running shaders).
        """
        shaders = self.started_shaders
        if shader_id not in shaders:
            return              # ignore if app disabled rendering

        added_to = shader_id.pop('added_to')
        shader_id.pop('rectangle')
        ren_ctx = shader_id.pop('render_ctx')
        if added_to:
            added_to.remove(ren_ctx)
        else:
            self.canvas = None

        if 'timer' in shader_id:
            Clock.unschedule(shader_id.pop('timer'))

        if stop:
            shader_id['mode'] = 'stop'

        shaders.remove(shader_id)


Factory.register('ShadersMixin', cls=ShadersMixin)
