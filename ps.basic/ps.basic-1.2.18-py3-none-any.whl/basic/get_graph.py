import inspect
from pprint import pformat

from ps.basic.State import StateError


def get_graph(fsm, title: str = None):
    """Generate a png/svg.

    Picture with dot - a graphviz executable.

    Have a look at the Usage section for a working example.

    :param fsm: [description]
    :type fsm: [type]
    :param title: [description], defaults to None
    :type title: str, optional
    :raises StateError: [description]
    :return: [description]
    :rtype: [type]
    """
    import pygraphviz as pgv

    fsm_dot_attrs = {
        "directed": True,
        "strict": False,
        "rankdir": "LR",
        "ratio": "0.3",
    }

    state_dot_attrs = {
        "shape": "circle",
        "height": "1.2",
    }

    dot_final = "doublecircle"

    title = fsm.name

    fsm_graph = pgv.AGraph(title=title, size="10.3, 5.3", **fsm_dot_attrs)
    fsm_graph.node_attr.update(state_dot_attrs)

    if fsm.init_state is None:
        raise StateError("A FSM must have a defined init_state")

    for state in [fsm.init_state] + fsm.states:
        color = "black"
        shape = state_dot_attrs["shape"]
        if hasattr(fsm, "final_states"):
            if id(state) in [id(s) for s in fsm.final_states]:
                shape = dot_final
        if hasattr(fsm, "error_states"):
            if id(state) in [id(s) for s in fsm.error_states]:
                color = "red"

        try:
            tooltip_str = pformat(inspect.getdoc(state.compute_function))
            state.tooltip = tooltip_str.replace("\\n", "&#013;")
        except AttributeError:  # pragma: no cover
            state.tooltip = "no tooltip"

        fsm_graph.add_node(
            n=state.name, shape=shape, color=color, tooltip=state.tooltip
        )
        if state.mail_addr:
            lis = eval(state.mail_addr)
            for d in lis:
                l2 = d.keys()
                name = list(l2)[0]
                value = d[name]
                fsm_graph.add_node(
                    n="EMAIL_DST" + name + value,
                    label="%s:%s" % (name, value),
                    shape="rpromoter",
                    style="filled",
                    fillcolor="lightseagreen:orangered",
                    color=color,
                    tooltip=state.tooltip,
                )
                fsm_graph.add_edge(
                    state.name,
                    "EMAIL_DST" + name + value,
                    penwidth=2,
                    label="send email ",
                    style="dashed",
                    color=color,
                    tooltip=state.tooltip,
                )

    fsm_graph.add_node("null", shape="plaintext", label=" ")
    fsm_graph.add_edge("null", fsm.init_state.name)

    for src, input_value, dst in fsm.all_transitions:
        label = str(input_value)
        fsm_graph.add_edge(src.name, dst.name, label=label)
    for state in fsm.states:
        if state.default_transition is not None:
            if id(state.default_transition) in \
                    [id(s) for s in fsm.error_states]:
                fsm_graph.add_edge(
                    state.name,
                    state.default_transition.name,
                    label="error",
                    color="red",
                    tooltip=state.tooltip,
                )
            else:
                fsm_graph.add_edge(
                    state.name,
                    state.default_transition.name,
                    label="else",
                    tooltip=state.tooltip,
                )

    return fsm_graph
