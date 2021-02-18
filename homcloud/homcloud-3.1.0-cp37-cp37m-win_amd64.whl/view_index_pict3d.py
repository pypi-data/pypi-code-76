import argparse

from homcloud.argparse_common import add_arguments_for_load_diagrams
from homcloud.version import __version__
from homcloud.view_index_pict import (
    predicate_from_string, use_vectorized_histogram_mask, histogram_mask_predicate,
    all_true, pairs_positions, load_idiagram_or_pdgm
)
from homcloud.visualize_3d import ParaViewSparseBitmapDrawer


def main(args=None):
    args = args or argument_parser().parse_args()
    pd = load_idiagram_or_pdgm(args.diagram, args.type, args.degree, args.negate)

    predicates = [predicate_from_string(string) for string in args.filter]
    if use_vectorized_histogram_mask(args):
        predicates.append(histogram_mask_predicate(args))

    pairs = [pair for pair in pairs_positions(pd) if all_true(predicates, pair)]
    drawer = ParaViewSparseBitmapDrawer(6, {"birth": None, "death": None})

    birth_color = drawer.various_colors[0]
    death_color = drawer.various_colors[4]

    for pair in pairs:
        if args.birth:
            drawer.draw_voxel(pair.birth_pos, birth_color, birth=1, death=0)
        if args.death:
            drawer.draw_voxel(pair.death_pos, death_color, birth=0, death=1)

    if args.vtk_output:
        drawer.output(args.vtk_output)


def argument_parser():
    p = argparse.ArgumentParser(description="Show birth and death cubes in 3D space")
    p.add_argument("-V", "--version", action="version", version=__version__)
    add_arguments_for_load_diagrams(p)
    p.add_argument("-f", "--filter", action="append", default=[],
                   help="filters (ex: \"lifetime > 5.0\")")
    p.add_argument("-v", "--vectorized-histogram-mask",
                   help="0-1 vector textfile for mask")
    p.add_argument("-H", "--histoinfo",
                   help="vectorize histogram information (both -V and -H are required)")
    p.add_argument("-B", "--birth", default=False, action="store_true",
                   help="plot birth pixels")
    p.add_argument("-D", "--death", default=False, action="store_true",
                   help="plot death pixels")
    p.add_argument("--vtk-output", help="output in vtk format")
    p.add_argument("diagram", help="persistence diagram file name")
    return p


if __name__ == "__main__":
    main()
