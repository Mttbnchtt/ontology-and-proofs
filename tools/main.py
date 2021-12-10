__title__ = "Formal ontology of math"
__author__ = "Matteo Bianchetti"
__date__ = "2021-20"
__version__ = "0.1"

import argparse
import sys
import textwrap

from modules.import_script import main as import_script


def parse(args_lst:list=[]):
    # create the parser
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
            --------------
            Execute some of the following:
            - import allDifferent steps (import, --type allDifferent, --input, --output, --verbose <True, False>)
            - import dependencies of steps (import, --type dependencies, --input, --output, --verbose <True, False>)
            - import individuals (import, --type individuals, --input, --output, --verbose <True, False>)
            - import links of steps to proofs (import, --type forProof, --input, --output, --verbose <True, False>)
            - import proof steps (import, --type step, --input, --output, --verbose <True, False>)
            --------------
            """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            For further help, open an issue on\ 
            https://github.com/Mttbnchtt/ontology-and-proofs""")
    )
    #add the arguments
    subparser = parser.add_subparsers(
        dest="command", #name of the attribute under which the
                        #sub-command name will be stored
        required=True)
    import_script = subparser.add_parser("import")
    # import
    import_script.add_argument(
        "-t",
        "--type",
        type=str,
        required=True,
        help="name of the input file"
    )
    import_script.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="name of the input file"
    )
    import_script.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="name of the output file"
    )
    import_script.add_argument(
        "-v",
        "--verbose",
        type=bool,
        required=False,
        choices={True, False, ""},
        default=False,
        help="verbose terminal message"
    )
    return parser.parse_args(args_lst) # the object returned by parse_args() 
                                # contains only attributes for the main 
                                # parser and the selected subparser

def main(args_lst:list):
    cmd_options:dict = {
        "import": import_script
    }
    args = parse(args_lst)
    if args.command not in cmd_options:
        raise ValueError(f"""
        Must choose one of the following commands
        {''.join(cmd_options)}""")
    cmd_options[args.command](args)


if __name__ == "__main__":
    main(sys.argv[1:] if len(sys.argv)>1 else ["--help"])