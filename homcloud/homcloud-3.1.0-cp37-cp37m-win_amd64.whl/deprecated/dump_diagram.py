from homcloud.index_map import MapType
from homcloud.diagram import PD

import homcloud.dump_diagram as dump_diagram


def output_diagram(args, output):
    diagram = PD.load_diagrams(args.type, [args.input], args.degree, args.negate)

    if diagram.filtration_type == MapType.abstract and args.show_simplices:
        write_pairs_with_positions(diagram, output, args.show_essential_pairs)
    elif args.symbols:
        if not args.show_simplices:
            raise (ValueError, "-s must be with -S option")
        if not diagram.index_map:
            raise (ValueError, ".idiagram file is required for -s option")
        write_pairs_with_symbolic_simplices(diagram, output, args.show_essential_pairs)
    elif diagram.filtration_type and args.show_simplices:
        write_pairs_with_positions(diagram, output, args.show_essential_pairs)
    else:
        dump_diagram.write_pairs(diagram, output, args.show_essential_pairs)


def write_pairs_with_positions(diagram, io, show_essential_pairs):
    if diagram.filtration_type in [MapType.bitmap, MapType.cubical]:
        formatter = format_pixel
    elif diagram.filtration_type == MapType.alpha:
        formatter = format_simplex
    elif diagram.filtration_type == MapType.abstract:
        def formatter(x):
            return x
    else:
        raise RuntimeError("Unkndown index map format")

    for (birth, death, birth_pos, death_pos) in zip(diagram.births,
                                                    diagram.deaths,
                                                    diagram.birth_positions,
                                                    diagram.death_positions):
        io.write("{} {} {} {}\n".format(birth, death,
                                        formatter(birth_pos), formatter(death_pos)))

    if show_essential_pairs:
        inf = dump_diagram.inf_string(diagram)
        for (birth, birth_pos) in zip(diagram.essential_births,
                                      diagram.essential_birth_positions):
            io.write("{} {} {} unavaliable\n".format(birth, inf, formatter(birth_pos)))


def write_pairs_with_symbolic_simplices(diagram, io, show_essential_pairs):
    geom_resolver = diagram.index_map.geometry_resolver(diagram)

    def format_simplex(idx):
        return " ".join(geom_resolver.cell_symbols(idx))

    for (birth_idx, death_idx) in zip(diagram.birth_indices, diagram.death_indices):
        birth_time = diagram.index_map.resolve_level(birth_idx)
        death_time = diagram.index_map.resolve_level(death_idx)
        if birth_time == death_time:
            continue
        print("{} {} ({}) ({})".format(
            birth_time, death_time, format_simplex(birth_idx), format_simplex(death_idx)
        ), file=io)

    if show_essential_pairs:
        inf = dump_diagram.inf_string(diagram)
        for birth_idx in diagram.essential_birth_indices:
            print("{} {} ({}) unavailable".format(
                diagram.index_map.resolve_level(birth_idx), inf, format_simplex(birth_idx)
            ), file=io)


def format_pixel(at):
    return "(" + ",".join([str(x) for x in at]) + ")"


def format_simplex(vertices):
    return "{" + ",".join([format_pixel(vertex) for vertex in vertices]) + "}"
