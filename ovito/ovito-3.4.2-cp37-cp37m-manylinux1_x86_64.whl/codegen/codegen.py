import inspect
import numpy
import collections.abc
import ovito

def format_property_value(value):
    """ Produces a pretty string representation of a Python object or value. """

    # Format small NumPy arrays as Python lists.
    if isinstance(value, numpy.ndarray):
        # Linear arrays of length 4 and shorter.
        if value.ndim == 1 and len(value) <= 4:
            return repr(value.tolist())
        # Matrix arrays of shape (3,4).
        if value.shape == (3,4):
            return repr(value.tolist())

    # Make sure the fully qualified type name is being used.
    t = type(value)
    if t.__name__ != t.__qualname__:
        result = repr(value)
        if result.startswith(t.__name__):
            result = t.__qualname__ + result[len(t.__name__):]
        return result
        
    # In all other cases, fall back to standard formatting using repr() function.
    return repr(value)

def property_value_diff(ref_value, value, include_vis, force_instantiation = False, prefer_oneliner = False):
    """ Compares two objects or values of the same type for equality. """

    # NumPy arrays cannot be compared using the == operator. Need to use array_equal() function instead.
    if isinstance(ref_value, numpy.ndarray) and isinstance(value, numpy.ndarray):
        if not numpy.array_equal(ref_value, value):
            return [" = {}".format(format_property_value(value))]
        else:
            return []

    # Implement element-wise deep comparison for list-like sequence types.
    if isinstance(ref_value, collections.abc.Sequence) and isinstance(value, collections.abc.Sequence) and not isinstance(ref_value, (tuple, str)):
        result = []
        if len(ref_value) == len(value): 
            for index, (ref_item, item) in enumerate(zip(ref_value, value)):
                for diff in property_value_diff(ref_item, item, include_vis, prefer_oneliner=prefer_oneliner):
                    result.append("[{}]{}".format(index, diff)) 
        elif len(ref_value) < len(value) and isinstance(value[0], ovito.plugins.PyScript.RefTarget): 
            for index, (ref_item, item) in enumerate(zip(ref_value, value[:len(ref_value)])):
                for diff in property_value_diff(ref_item, item, include_vis, prefer_oneliner=prefer_oneliner):
                    result.append("[{}]{}".format(index, diff)) 
            for item in value[len(ref_value):]:
                if isinstance(item, ovito.plugins.PyScript.RefTarget):
                    statements = generate_object_instantiation("obj", None, item, include_vis)
                    if isinstance(statements, str):
                        # Generate in-place modifier instantiation:
                        result.append(".append({})".format(statements))
                    else:
                        # Generate code with a temporary variable:
                        result.append("\n".join(statements) + "\n.append(obj)")
                else:
                    result.append(".append({})".format(format_property_value(item)))
        else:
            result.append(" = {}".format(format_property_value(value)))
        return result

    # Compare two OVITO objects based on their attributes.
    if (ref_value is None or isinstance(ref_value, ovito.plugins.PyScript.RefTarget)) and (value is None or isinstance(value, ovito.plugins.PyScript.RefTarget)):
        result = []
        if type(ref_value) is not type(value) or force_instantiation:
            result.append(" = {}".format(format_property_value(value)))
        if value is None:
            return result
        only_property_assignments = (len(result) == 1)
        for attr_name, attr_value in get_object_modified_properties(ref_value, value, include_vis).items():
            for diff in attr_value:
                result.append(".{}{}".format(attr_name, diff))
                if not diff.startswith(" = "): only_property_assignments = False

        # If the statements are direct property value assignments, 
        # reformat it as a single constructor call.
        if only_property_assignments:
            arguments = []
            for stat in result[1:]:
                arg = stat[1:]
                if not prefer_oneliner and len(result) > 2:
                    arg = "\n    " + arg
                arguments.append(arg)
            result = [" = {}({})".format(type(value).__qualname__, ", ".join(arguments))]

        return result

    # Use built-in comparison operator otherwise.
    if ref_value != value:
        return [" = {}".format(format_property_value(value))]

    return []

def generate_object_instantiation(variable_name, ref_obj, obj, include_vis = False, prefer_oneliner = False):
    """ Generates code that instantiates a new object and sets its parameters. """
    assert(isinstance(obj, ovito.plugins.PyScript.RefTarget))

    statements = property_value_diff(ref_obj, obj, include_vis, force_instantiation=True, prefer_oneliner=prefer_oneliner)
    if len(statements) == 1:
        # Generate one-liner.
        assert(statements[0].startswith(" = "))
        return statements[0][len(" = "):]
    else:
        src_lines = []
        for stat in statements:
            src_lines.append("{}{}".format(variable_name, stat))
        return src_lines

def get_object_modified_properties(ref_obj, obj, include_vis = False):
    """ Builds a list of properties of the given object which were modified by the user. """ 

    # Unless the caller has already provided it, create a default-initialized object instance of the same type as the input object.
    # It will be used to detect which object parameters were modified by the user.
    if not ref_obj:
        ref_obj = type(obj)()

    # Iterate over all attributes of the input object.
    attr_list = {}
    for attr_name in obj.__dir__():
        # Determine if the attribute is an object property.
        attr = inspect.getattr_static(obj, attr_name)
        if isinstance(attr, property):
            
            # Skip hidden object attributes which are not documented.
            if not attr.__doc__: continue

            # Get the property value.
            value = getattr(obj, attr_name)
            # Get the corresponding value of the default-initialized reference object.
            ref_value = getattr(ref_obj, attr_name)

            # Skip visualization elements unless they should be included and are not disabled.
            if isinstance(value, ovito.vis.DataVis) and include_vis == False:
                continue

            # Skip data objects.
            if isinstance(value, ovito.data.DataObject):
                continue

            # Add attribute to the output list if its value does not exactly match the default value.
            diff = property_value_diff(ref_value, value, include_vis)
            if diff:
                attr_list[attr_name] = diff

    if hasattr(obj, "__codegen__"):
        # Give all classes in the hierarchy the chance to filter or amend the generated statements.
        clazz = type(obj)
        while clazz is not ovito.plugins.PyScript.RefTarget:
            if "__codegen__" in clazz.__dict__:
                clazz.__codegen__(obj, attr_list)
            clazz = clazz.__bases__[0]

    return attr_list

def codegen_modifier(modifier, include_vis):
    """ Generates code lines for setting up a modifier and its parameters. """

    # Special handling for PythonScriptModifier:
    if isinstance(modifier, ovito.modifiers.PythonScriptModifier):
        # Do not emit code if Python script modifier is disabled.
        if not modifier.enabled: 
            return "\n\n# Skipping disabled modifier '{}'".format(modifier.object_title)

        # Simply output the script source code entered by the user. 
        src = "\n\n# User-defined modifier '{}':\n".format(modifier.object_title)
        src += modifier.script
        if not modifier.kwargs:
            src += "\npipeline.modifiers.append(modify)"
        else:
            # Pass the values of the user-defined parameters to the modifier function using
            # partial function parameter binding.
            src += "\nimport functools"
            kwargs_list = []
            for key,value in modifier.kwargs.items():
                if isinstance(value, ovito.plugins.PyScript.RefTarget):
                    statements = generate_object_instantiation(key, type(value)(), value, include_vis, prefer_oneliner=True)
                else:
                    statements = format_property_value(value)
                if isinstance(statements, str):
                    # Generate in-place instantiation:
                    kwargs_list.append("{} = {}".format(key, statements))
                else:
                    # Generate code with a temporary variable:
                    src += "\n" + "\n".join(statements) 
                    kwargs_list.append("{} = {}".format(key,key))

            if len(kwargs_list) > 2:
                kwargs_list = ["\n    " + arg for arg in kwargs_list]

            src += "\npipeline.modifiers.append(functools.partial(modify, {}))".format(", ".join(kwargs_list))
        return src 

    # Create a default-initialized modifier instance.
    # It will be used to detect which modifier parameters were modified by the user.
    default_modifier = type(modifier)()

    # Temporarily insert it into a pipeline in order to let the modifier initialize itself based on the current pipeline state.
    modapp = modifier.some_modifier_application
    if modapp:
        default_modapp = default_modifier.create_modifier_application()
        default_modapp.input = modapp.input
        default_modapp.modifier = default_modifier
        default_modifier.initialize_modifier(default_modapp)

    src = "\n\n# {}:\n".format(modifier.object_title)
    statements = generate_object_instantiation("mod", default_modifier, modifier, include_vis)
    if isinstance(statements, str):
        # Generate in-place modifier instantiation:
        return src + "pipeline.modifiers.append({})".format(statements)
    else:
        # Generate code with a temporary variable:
        return src + "\n".join(statements) + "\npipeline.modifiers.append(mod)"

def find_visual_element_prefix_recursive(obj, vis):
    """ Recursively searches a given visual element in the object hierarchy of a DataCollection. """  
    result = None
    for attr_name in obj.__dir__():

        # Determine if the attribute is an object property.
        attr = inspect.getattr_static(obj, attr_name)
        if isinstance(attr, property):
            
            # Skip underscore property fields.
            if attr_name.endswith("_"): continue

            # Skip hidden object attributes which are not documented.
            if not attr.__doc__: continue

            # Access the property value.
            try:
                value = getattr(obj, attr_name)
                if value is vis:
                    # We have found the visual element in the object hierarchy.
                    result = "." + attr_name
                    break

                if not result and isinstance(value, ovito.plugins.PyScript.RefTarget):
                    # Continue with recursive search.
                    path = find_visual_element_prefix_recursive(value, vis)
                    if path:
                        result = "." + attr_name + path
            except KeyError:
                pass
    return result

def find_visual_element_prefix(pipeline, vis):
    """ Builds the hierarchical Python object expression that references the given visual element in a DataCollection. """  
    if not pipeline.source: 
        return None
    return find_visual_element_prefix_recursive(pipeline.source.data, vis)

def codegen_pipeline(pipeline, include_vis):
    """ Generates Python statements for setting up a data pipeline. """

    # Generate script header.
    src = "# Boilerplate code generated by OVITO Pro {}\n".format(ovito.version_string)
    src += "from ovito.io import *\n"
    src += "from ovito.modifiers import *\n"
    src += "from ovito.pipeline import *\n"
    if include_vis:
        src += "from ovito.vis import *\n"

    # Generate call to import_file() creating the Pipeline object.
    if isinstance(pipeline.source, ovito.pipeline.FileSource):
        src += "\n# Data import:\n"
        # Ask the pipeline's FileSource to compile the list of arguments to be passed to the 
        # import_file() function. 
        filesource_attrs = {}
        pipeline.source.__codegen__(filesource_attrs)
        # Note: FileSource.__codegen__() would normally generate a call to the FileSource.load() method.
        # Here we just take the call argument list and use it to generate a call to import_file() instead. 
        src += "pipeline = import_file{}".format(filesource_attrs["load"][0])

    # Generate statements for setting up the visual elements of the import data.
    if include_vis:
        src += "\npipeline.add_to_scene()"
        has_visual_element_setup = False
        for vis in pipeline.vis_elements:
            
            prefix = find_visual_element_prefix(pipeline, vis)
            if not prefix: continue

            for attr_name, attr_diff in get_object_modified_properties(None, vis, True).items():
                for diff in attr_diff:
                    if not has_visual_element_setup:
                        has_visual_element_setup = True
                        src += "\n\n# Configuring visual elements associated with imported dataset:"
                    src += "\npipeline.compute(){}.{}{}".format(prefix, attr_name, diff)

    # Generate statements for creating the modifiers in the pipeline.
    for modifier in pipeline.modifiers:

        # Skip hidden modifier types which are not documented.
        if not modifier.__doc__: 
            src += "\n\n# Skipping modifier '{}'".format(modifier.object_title)
            continue

        src += codegen_modifier(modifier, include_vis)

    # Generate statements for setting up a viewport.
    if include_vis and ovito.scene.viewports.active_vp:

        # Generate statement for creating and configuring the Viewport instance.
        src += "\n\n# Viewport setup:"
        for stat in property_value_diff(None, ovito.scene.viewports.active_vp, True, force_instantiation=True):
            src += "\nvp{}".format(stat)

        # Generate statement for setting up the renderer.
        rs = ovito.scene.render_settings
        statements = property_value_diff(None, rs.renderer, True, force_instantiation=True)
        has_renderer = False
        if len(statements) > 1 or statements[0] != " = OpenGLRenderer()":
            has_renderer = True
            src += "\n\n# Renderer setup:"
            for stat in statements:
                src += "\nrenderer{}".format(stat)

        # Generate call to render_image() or render_anim().
        src += "\n\n# Rendering:\n"
        args = []
        args.append("size={!r}".format(rs.size))
        if rs.background_color != (1.0, 1.0, 1.0):
            args.append("background={!r}".format(rs.background_color))        
        if rs.generate_alpha:
            args.append("alpha=True")
        if has_renderer:
            args.append("renderer=renderer")
        if rs.range == ovito.plugins.PyScript.RenderSettings.Range.CurrentFrame:
            args.insert(0, "filename={!r}".format(rs.output_filename if rs.output_filename else 'image.png'))
            if ovito.scene.anim.current_frame != 0:
                args.append("frame={}".format(ovito.scene.anim.current_frame))
            src += "vp.render_image({})".format(", ".join(args))
        else:
            args.insert(0, "filename={!r}".format(rs.output_filename if rs.output_filename else 'movie.mp4'))
            args.append("fps={!r}".format(ovito.scene.anim.frames_per_second))
            if rs.range == ovito.plugins.PyScript.RenderSettings.Range.CustomInterval:
                args.append("range={!r}".format(rs.custom_range))
            if rs.every_nth_frame > 1:
                args.append("every_nth={!r}".format(rs.every_nth_frame))
            src += "vp.render_anim({})".format(", ".join(args))

    return src

if __name__ == "__main__":
    
    from ovito.io import *
    from ovito.modifiers import *
    from ovito.vis import *
    from ovito.pipeline import *
#    print(codegen_pipeline(ovito.scene.selected_pipeline, True))