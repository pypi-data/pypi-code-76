#from abc import ABC, abstractmethod

class TagDef:
    tag_name = None
    add_to_collector = False
    is_toc_section = False
    is_context = False
    is_pre = False
    is_root = False

    allow_children = None
    exclude_children = None

    # maybe use type or issubclasss instead?
    is_element = True

    def __init__(self, line_no, indent_level, parent, order, nth_of_type, trim_left, trim_right):
        self.trim_left = trim_left
        self.trim_right = trim_right

        self.line_no = line_no
        self.indent_level = indent_level
        self.parent = parent
        self.order = order
        self.nth_of_type = nth_of_type
        self.trim_left = trim_left
        self.trim_right = trim_right

        # modified directly
        self.children = []
        self.collectors = {}
        self.content = ''
        self.context = {}
        self.extra_context = {}

        self.tag_id = f'{self.tag_name}-{self.nth_of_type}'


    @classmethod
    def init_as_root(cls):
        if not cls.is_root:
            raise Exception(f"Cannot init non-root TagDef '{cls.__name__}' as root")
        return cls(None, None, None, 0, 0, False, False)


    @classmethod
    def is_child_allowed(cls, child_tag_name):
        if cls.is_pre:
            return False
        elif cls.allow_children is not None:
            return child_tag_name in cls.allow_children
        else:
            return child_tag_name not in cls.exclude_children

    @classmethod
    def check(cls, tag_dict):
        allow_val = cls.allow_children
        exclude_val = cls.exclude_children

        def_ref = f"TagDef '{cls.__name__}'"

        for val, attr in ((allow_val, 'allow_children'), (exclude_val, 'exclude_children')):
            if val is not None and type(val) not in (list, tuple):
                raise Exception(f'{def_ref} specifies invalid value for {attr}. Must be None or tuple/list of tag names')

        if cls.is_pre:
            #if allow_val or (exclude_val is False) or (exclude_val and exclude_val_type is not bool):
            if allow_val or exclude_val is not None:
                raise Exception(f'{def_ref} has is_pre=True. Pre tags cannot have children and exclude all tags by default. Remove the allow/exclude_children values from this def to use the default or explicitly set allow_children=[]')
        elif allow_val is None and exclude_val is None:
            raise Exception(f'{def_ref} must specify a value for either allow_children OR exclude_children')
        elif (allow_val is not None and exclude_val is not None):
            raise Exception(f'{def_ref} must specify a value for either allow_children OR exclude_children, not both')
        else:
            check_list = allow_val or exclude_val
            if check_list:
                # TODO use set.difference for this?
                for tag_name in check_list:
                    if tag_name not in tag_dict:
                        attr_name = 'allow' if check_list is allow_val else 'exclude'
                        raise Exception(f"{def_ref} contains an undefined tag name in {attr_name}_children: '{tag_name}'")


    #TODO useful for debugging, but not actually used in the rendering process
    def walk(self):
        rep = ''
        for x in self.children:
            rep += x.walk() + ', '
        return f'[{self.tag_name}, {rep[:-2]}]'


    # can be overriden to customize or perform additional formatting on context tags
    # (i.e. looking up urls based on blog entry PKs)
    def process_data(self, data):
        # empty tag (with no children) returns empty list. Use first value in list if it exists as a sane default
        return (data and data[0]) or ''


    def get_data(self):
        child_data = []
        for child in self.children:
            child_data.append(child.get_data())
        return {self.tag_name: self.process_data(child_data)}


    def pre_render(self, root, extra_context={}):
        for child in self.children:
            child.pre_render(root, extra_context)

        if self.is_context:
            self.parent.context.update(self.get_data())

        self.extra_context = extra_context

        if self.add_to_collector:
            root.collectors.setdefault(self.tag_name, []).append(self.render(False))


    def render(self, main=True):
        rendered_children = []
        prev_child = None

        for child in self.children:
            child_rendered = child.render(main)

            if child_rendered:
                no_whitespace = (prev_child and prev_child.trim_right) or child.trim_left
                if rendered_children and not no_whitespace:
                    rendered_children.append('\n')

                rendered_children.append(child_rendered)

            prev_child = child

        self.content = ''.join(rendered_children)
        return self.render_main() if main else self.render_secondary()


    def render_main(self):
        # TODO is this a sane default?
        return '' if self.is_context else self.content


    def render_secondary(self):
        # TODO is this a sane default?
        return self.render_main()

    def add_child_element(self, defs_manager, tag_name, value):

        tag_def = defs_manager.get_def(tag_name)
        if tag_def is None:
            raise Exception(f"Not a defined tag_name: {tag_name}")

        if tag_name not in self.allow_children:
            def_ref = f"TagDef '{self.__class__.__name__}'"
            raise Exception(f"Child tag '{tag_name}' not allowed as child of {def_ref}")

        # TODO just use None for values that can't be calculated. A bit hackish, but will
        # be fine to just re-generate the dentmark code. Not going to render this tree
        tag_def_inst = tag_def(None, None, self, len(self.children), None, False, False)

        from dentmark.text_node import TextNode

        text_node_inst = TextNode(None, None, tag_def_inst, 0, value)
        tag_def_inst.children.append(text_node_inst)
        self.children.append(tag_def_inst)


    def get_tag_by_id(self, tag_id):
        if self.tag_id == tag_id:
            return self

        for child in self.children:
            if not child.is_element:
                continue
            found_it = child.get_tag_by_id(tag_id)
            if found_it:
                return found_it
        return None


    def gen_tags_by_name(self, tag_name):
        if self.tag_name == tag_name:
            yield self

        for child in self.children:
            if not child.is_element:
                continue
            for found in child.gen_tags_by_name(tag_name):
                yield found

    def get_child_by_name(self, tag_name, return_multiple=False):
        multiple = []
        for child in self.children:
            if not child.is_element:
                continue
            if child.tag_name != tag_name:
                continue
            if not return_multiple:
                return child
            multiple.append(child)
        return multiple if return_multiple else None


    # experiment with generating dentmark markup from the tree,
    # so that eventually we can edit the tree, then output modified dentmark
    def to_dentmark(self, indent_level = 0):

        # make sure tags with no children like br: have a trailing newline
        children_str = '' if self.children else '\n'

        for i, child in enumerate(self.children):
            if i == 0:
                if (not self.is_pre) and (not child.is_element):
                    # If first child is a text node, print it inline with tag to preserve
                    # intentional 'tag masking' i.e. a: https://
                    # This also saves space anyways even if tag masking is not necessary.
                    children_str += f' {child.text}\n'
                    continue
                children_str += '\n'

            children_str += child.to_dentmark(indent_level + (not self.is_root))

        tab = ' ' * (indent_level * 4)
        trim_left = '-' if self.trim_left else ''
        trim_right = '-' if self.trim_right else ''

        if self.is_root:
            return f'{children_str}'
        else:
            return f'{tab}{trim_left}{self.tag_name}{trim_right}:{children_str}'
