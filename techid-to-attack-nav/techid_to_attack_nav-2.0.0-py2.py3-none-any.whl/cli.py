"""Console script for techid_to_attack_nav."""
import argparse
import sys
from techid_to_attack_nav.core import * 


def main():
    """Console script for techid_to_attack_nav."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_file", help="Specify the input file that contains technique IDs")
    parser.add_argument(
        "-n", "--name", help="Specify the actor or tool name for the title of the resulting layer")
    parser.add_argument("-t", "--template_file",
                        help="Specify the ATT&CK Navigator layer .JSON template you would like to use", default="default")
    parser.add_argument("-o", "--output_file",
                        help="Specify the file for the resulting template layer .JSON content", default="results.json")
    args = parser.parse_args()

    techniques = extract_techniques(args.input_file)
    template = get_template(args.template_file)
    set_actor(args.name, template)
    align_ttps(template, techniques)
    write_template(template, args.output_file)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
