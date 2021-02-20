# python standard imports
from argparse import ArgumentParser
from pathlib import Path
# internal imports
from . import Exhibit, evidence_in_dir, write_pdf, write_list

# global variables
DEFAULT_OUTPUT_PDF = './Exhibits.pdf'
DEFAULT_OUTPUT_LIST = './Exhibit List.docx'

def cli():
    # Read command-line input
    parser = ArgumentParser(description="This program processes "
        + "evidence for discovery responses and jury trials. Give it a "
        + "folder containing one or more subfolders that represent "
        + "exhibits, and it will generate a PDF containing all the "
        + "evidence, and a Word document listing it. For more info, see "
        + "https://github.com/raindrum/exhibiter.")
    parser.add_argument(
        "input",
        help="path to a folder containing exhibits.")
    parser.add_argument(
        "-o", "--output-files",
        help="specify where to save the two output files, respectively. "
            + f"Defaults to '{DEFAULT_OUTPUT_PDF} {DEFAULT_OUTPUT_LIST}'.",
        action="store",
        nargs=2,
        default=[DEFAULT_OUTPUT_PDF, DEFAULT_OUTPUT_LIST],
        metavar=("PDF_FILE", "DOCX_FILE"))
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help='include files marked "(EXCLUDE)" and "(UNUSED)"')
    parser.add_argument(
        "-n", "--no-page-numbers",
        action="store_true",
        help="don't add page number labels to the output PDF")
    parser.add_argument(
        "-k", "--keep-leading-digits",
        action="store_true",
        help="don't strip leading numbers (e.g. \"1. \") from document names")
    parser.add_argument(
        "-c", "--page-label-coords",
        nargs=2,
        help="the X and Y position of the page number printed on "
             + "PDF pages, expressed as percentages of the page, "
             + "starting from the left and bottom. Defaults to %(default)s",
        default=(50, 3),
        metavar=("X", "Y"),
        type=int)
    parser.add_argument(
        "-p", "--party",
        action="store",
        help="the party whose exhibit list this is. Defaults to defendant.",
        type=str,
        choices=['defendant', 'plaintiff'])
    parser.add_argument(
        "-r", "--no-reserve-rebuttal",
        action="store_true",
        help="in the exhibit list, don't reserve an exhibit for rebuttal")
    parser.add_argument(
        "-l", "--allow-landscape",
        action="store_true",
        help="don't rotate landscape photos in order to fill the page better")
    parser.add_argument(
        "--attachno",
        help="which trial document attachment the exhibit list is. Defaults "
            + "to 4.",
        type=int,
        default=4)
    args = parser.parse_args()

    # Ensure input folder exists and contains exhibits
    input_dir = Path(args.input)
    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' is not a real folder.")
        return
    exhibit_paths = evidence_in_dir(input_dir, not args.all)
    if not exhibit_paths:
        print(f"Error: Input folder '{input_dir}' contains no exhibits, "
            + "or they are all marked for exclusion.")

    # add all exhibits
    exhibits = []
    for path in exhibit_paths:
        exhibits.append(Exhibit.from_path(
            path,
            respect_exclusions=not args.all,
            number_pages=not args.no_page_numbers,
            page_label_coords=args.page_label_coords,
            rotate_landscape_pics=not args.allow_landscape,
            strip_leading_digits=not args.keep_leading_digits))

    # Write output files
    write_pdf(exhibits, args.output_files[0])
    write_list(
        exhibits,
        args.output_files[1],
        attachment_no = args.attachno,
        party_label="Plaintiff" if args.party == "plaintiff" else "Defense",
        show_page_numbers=not args.no_page_numbers,
        reserve_rebuttal=not args.no_reserve_rebuttal)
