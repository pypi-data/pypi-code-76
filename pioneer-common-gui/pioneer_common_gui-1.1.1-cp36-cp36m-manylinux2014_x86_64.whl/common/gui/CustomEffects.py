from pioneer.common.gui import Effect, Array

from PyQt5.QtGui import QColor, QVector4D, QVector3D, QVector2D

import numpy as np

def point_colors(line_width = 1, point_size = 1):
    return Effect.Effect(name = "point_colors"
    , line_width = line_width
, point_size = point_size
, shader0 = Effect.GLSLProgram( 
            vertex_shader = 
            """
                #version 410
                uniform highp mat4 matrix;
                uniform highp float point_size;
                in highp vec4 vertices;
                in highp vec4 colors;

                out vec4 color;
                void main()
                {
                    gl_Position = matrix*vertices;
                    gl_PointSize = point_size;
                    color = colors;
                }
            """
            , fragment_shader = 
            """
                #version 410
                in vec4 color;
                layout(location = 0) out vec4 frag_color;
                layout(location = 1) out vec4 frag_color_copy;
                void main()
                {
                    frag_color_copy = frag_color = color;
                }
            """
            ))
def color_map(color_map, min_amplitude, max_amplitude, back_color = QColor("red")):

    return Effect.Effect(name = "color_map"
    , shader0 = Effect.GLSLProgram( 
    vertex_shader = """
                        #version 410
                        uniform highp mat4 matrix;
                        uniform highp float point_size;
                        in highp vec4 vertices;
                        in highp vec3 normals;
                        in highp float amplitude;

                        out float a;
                        void main()
                        {
                            gl_Position = matrix*vertices;
                            gl_PointSize = point_size;
                            a = amplitude;
                        }
                   """
    , fragment_shader = """
                        #version 410
                        uniform sampler1D color_map;
                        uniform highp vec4 back_color;
                        uniform highp float min_amplitude;
                        uniform highp float max_amplitude;
                        in float a;
                        layout(location = 0) out vec4 frag_color;
                        layout(location = 1) out vec4 frag_color_copy;
                        void main()
                        {
                            if (gl_FrontFacing) // is the fragment part of a front face?
                            {
                                frag_color = texture(color_map, max((a - min_amplitude), 0)/(max_amplitude-min_amplitude));
                            }
                            else // fragment is part of a back face
                            {
                                frag_color = vec4(back_color.x * a, back_color.y * a, back_color.z * a, back_color.w);
                            }

                            frag_color_copy = frag_color;
                        }
                    """
    , uniforms = {'back_color' : back_color, 'min_amplitude' : min_amplitude, 'max_amplitude' : max_amplitude}
    , textures = {'color_map' : color_map}
    ))

def emissive(color, back_color = QColor("red"), line_width = 1, point_size = 1, is_billboard = False):
    return Effect.Effect(name = "emissive"
    , line_width = line_width
    , point_size = point_size
    , shader0 = Effect.GLSLProgram(
        vertex_shader = """ 
                            #version 410
                            in highp vec4 vertices;
                            in highp vec3 normals;
                            uniform bool is_billboard;

                            uniform float aspect_ratio;
                            uniform mat4 model_matrix, view_matrix, projection_matrix;
                            uniform mat4 view_matrix_inv;
                            void main()
                            {
                                mat4 mv = view_matrix*model_matrix;
                                if(is_billboard)
                                {
                                    //https://gist.github.com/mattdesl/67838c69c22218242cadf4f5d0721d42
                                     vec2 scale = vec2(
                                         length(mv[0]) / aspect_ratio,
                                         length(mv[1])
                                     );
                                     vec4 billboard = mv * vec4(vec3(0.0), 1.0);

                                     gl_Position = projection_matrix * billboard + vec4(scale.xy * vertices.xy, 0.0, 0.0);
                                }
                                else
                                    gl_Position = projection_matrix*mv*vertices;
                            }
                    """
        , fragment_shader = """
                            #version 410
                            uniform highp vec4 color;
                            uniform highp vec4 back_color;
                            layout(location = 0) out vec4 frag_color;
                            layout(location = 1) out vec4 frag_color_copy;
                            void main()
                            {
                                if (gl_FrontFacing) // is the fragment part of a front face?
                                {
                                    frag_color = color;
                                }
                                else // fragment is part of a back face
                                {
                                    frag_color = back_color;
                                }
                                frag_color_copy = frag_color;
                            }
                        """
        , uniforms = {'color' : color, 'back_color' : back_color, 'is_billboard' : is_billboard}))


def depth(scale = 0.01):
    return Effect.Effect( name = "depth"
    , shader0 = Effect.GLSLProgram(
        uniforms = {'scale' : scale}
        # , outputTextures = {'float_depth': Array.Array(ndarray = np.empty((0,0,4), np.uint8))}
        , vertex_shader = """ 
                            #version 410
                            in highp vec4 vertices;
                            in highp vec3 normals;
                            uniform mat4 model_matrix, view_matrix, projection_matrix;
                            out float dist_to_camera;
                            out vec4 cam_coord;

                            void main()
                            {   
                                mat4 mv = view_matrix*model_matrix;
                                cam_coord = mv * vertices;
                                dist_to_camera = cam_coord.z;
                                gl_Position = projection_matrix * cam_coord;
                            }
                    """
        , fragment_shader = """
                            #version 410
                            uniform float scale;
                            uniform mat4 projection_matrix;
                            uniform mat4 ortho_matrix;
                            in vec4 cam_coord;
                            in float dist_to_camera;
                            layout(location = 0) out vec4 frag_color;
                            layout(location = 1) out vec4 float_depth;

                            // https://www.khronos.org/opengl/wiki/Compute_eye_space_from_window_space
                            float linearize_depth(float depth) 
                            {
                                float z_ndc = (depth * 2.0 - gl_DepthRange.near - gl_DepthRange.far)/(gl_DepthRange.far - gl_DepthRange.near); // back to NDC 
                                return  projection_matrix[3][2] / (z_ndc - (projection_matrix[2][2] / projection_matrix[2][3]));	
                            }

                            vec4 packFloatToVec4i(const float value) 
                            {
                                //http://marcodiiga.github.io/encoding-normalized-floats-to-rgba8-vectors
                                const vec4 bitSh = vec4(256.0*256.0*256.0, 256.0*256.0, 256.0, 1.0);
                                const vec4 bitMsk = vec4(0.0, 1.0/256.0, 1.0/256.0, 1.0/256.0);
                                vec4 res = fract(value * bitSh);
                                res -= res.xxyz * bitMsk;
                                return res;
                            }


                            void main()
                            {
                                float d = linearize_depth(gl_FragCoord.z); //;
                                frag_color = vec4(vec3(linearize_depth(gl_FragCoord.z)), 1.0);
                                float_depth = packFloatToVec4i(d);
                            }
                        """
        ))



def material(color = QColor("red")
, back_color = QColor("red")
, ambient_color = QColor.fromRgbF(.4, .4, .4, 1.0)
, specular_color = QColor.fromRgbF(.4, .4, .4, 1.0)
, light_power = 2e5
, shininess = 0.1
, light_follows_camera = True
, light_position = QVector3D(0,0,-10)
, reverse_backfaces = True):
    '''
    \param color                  front faces color
    \param back_color             back faces color
    \param shininess              material specular reflection ratio parameter [0, 1.0]
    \param light_follows_camera   if True, the light position is assigned camera's position, else \a light_position is used 
    \param light_position         light_follows_camera is False:
                                - light_position.xyz define light's position
                                - if light_position.w == 0.0, light is a spot light, else light is an omni-diretional light
    \param spot_direction         if light_follows_camera is False, and light_position.w == 0.0, defines spotlight's direction

    '''
    return Effect.Effect( name = "material"
    , shader0 = Effect.GLSLProgram(
        uniforms = {  'color' : color
                    , 'back_color' : back_color
                    , 'ambient_color': ambient_color
                    , 'specular_color': specular_color
                    , 'light_power': light_power
                    , 'shininess': shininess
                    , 'light_follows_camera': light_follows_camera
                    , 'light_position': light_position
                    , 'reverse_backfaces' : reverse_backfaces
                    }
        , vertex_shader = MATERIAL_VERTEX_SHADER
        , fragment_shader = MATERIAL_FRAGMENT_SHADER.format("color")
    ))

def textured_material(\
    textures #expects: {'diffuse': ndarray}, in the future we could add more samplers/texcoords pairs
, color = QColor("green")
, back_color = QColor("red")
, ambient_color = QColor.fromRgbF(.1, .1, .1, 1.0)
, specular_color = QColor.fromRgbF(.1, .1, .1, 1.0)
, light_power = 1e3 #light power should be roughly ("sight distance")^2
, shininess = 0.01
, light_follows_camera = True
, light_position = QVector3D(0,0,-10)
, reverse_backfaces = True):
    '''
    \param light_follows_camera   if True, the light position is assigned camera's position, else \a light_position is used 
    \param light_position         light_follows_camera is False:
                                - light_position.xyz define light's position
    '''
    return Effect.Effect( name = "textured_material"
        , shader0 = Effect.GLSLProgram(
        uniforms = { 'color': color #not used, meant to be diffuse color
                    , 'back_color' : back_color
                    , 'ambient_color': ambient_color
                    , 'specular_color': specular_color
                    , 'light_power': light_power
                    , 'shininess': shininess
                    , 'light_follows_camera': light_follows_camera
                    , 'light_position': light_position
                    , 'reverse_backfaces' : reverse_backfaces}
        , textures = textures
        , vertex_shader = MATERIAL_VERTEX_SHADER
        , fragment_shader = MATERIAL_FRAGMENT_SHADER.format("texture2D(diffuse, diffuse_tc.st)")
    ))

MATERIAL_VERTEX_SHADER = \
        '''
        #version 410
        //inspired from https://github.com/pycollada/pycollada/blob/master/examples/daeview/renderer/shaders.py
        in vec4 vertices;
        in vec3 normals;
        in vec2 texcoords0;

        uniform mat4 model_matrix, view_matrix, projection_matrix;
        uniform mat4 view_matrix_inv;

        uniform bool light_follows_camera;
        uniform vec3 light_position; // only used if light_follows_camera == false

        out vec3 normal_direction, light_direction, view_direction;
        out float distance;
        out vec2 diffuse_tc;

        void main()
        {
            normal_direction = vec3(model_matrix * vec4(normals, 0));

            vec3 vertex_position = vec3(model_matrix * vertices);

            vec3 eye_position = vec3(view_matrix_inv * vec4(0.0, 0.0, 0.0, 1.0));

            vec3 light_position_ = light_position;

            if(light_follows_camera)
                light_position_ = eye_position;

            light_direction = vec3(light_position_ - vertex_position);
            
            view_direction = eye_position - vertex_position;

            distance = length(view_direction);
            
            view_direction = normalize(view_direction);
            
            gl_Position = projection_matrix * view_matrix * model_matrix * vertices;

            diffuse_tc = texcoords0;
        }
        '''
MATERIAL_FRAGMENT_SHADER = \
        '''
        #version 410
        in vec3 normal_direction, light_direction, view_direction;
        in float distance;
        in vec2 diffuse_tc;
        uniform sampler2D diffuse;
        uniform float light_power;
        uniform float shininess;
        uniform vec4 color;
        uniform vec4 back_color;
        uniform vec4 ambient_color;
        uniform vec4 specular_color;
        uniform bool reverse_backfaces;
        layout(location = 0) out vec4 frag_color;
        layout(location = 1) out vec4 frag_color_copy;

        void main (void)
        {{
            vec4 final_color = back_color;

            //https://en.wikipedia.org/wiki/Phong_reflection_model

            vec3 N = normalize(normal_direction); //surface normal
            vec3 L = normalize(light_direction); //direction toward light source

            float lambertian = dot(L, N);


            if(reverse_backfaces && lambertian < 0.0)
            {{
                lambertian = -lambertian;
                N = -N;
            }}

            if(lambertian > 0.0)
            {{
                vec3 V = normalize(view_direction); //direction toward eye
                
                vec3 R = reflect(-L, N); 
                // reflect is a shortcut for I - 2*dot(N, I)*N, see https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/reflect.xhtml
                // we negate L since I stands for "incident light", L stands for "toward light source"

                float specular = pow( max( dot(R, V), 0.0), shininess );
                
                final_color = vec4({0}.xyz * light_power * (ambient_color.xyz * lambertian + specular_color.xyz * specular)/(distance*distance), 1);
            }}
            frag_color_copy = frag_color = final_color;
        }}
        '''