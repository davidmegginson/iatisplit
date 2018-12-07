from iatisplit.split import split
import sys, argparse, logging

logger = logging.getLogger(__name__)
"""Logger for this module"""


def main(args):
    """Entry point for a script.
    @args: a list of command-line arguments.
    """
    
    def parse_date(s):
        """Make sure we have an ISO YYYY-MM-DD date"""
        if re.match('^\d{4}-\d{2}-\d{2}$', s):
            return s
        else:
            raise Exception("Bad date format: {}".format(s))

    argsp = argparse.ArgumentParser(description="Split IATI activity files.")
    argsp.add_argument(
        '--max-activities', '-n',
        required=True,
        type=int,
        metavar="NUMBER",
        help="Maximum number of IATI activities to include in each output file."
    )
    argsp.add_argument(
        '--output-directory', '-d',
        required=False,
        default=".",
        metavar="path/to/output/directory",
        help="Put output files in this directory (instead of the current one)."
    )
    argsp.add_argument(
        '--output-stub', '-o',
        required=False,
        default=None,
        metavar="filename",
        help="Stub for creating output filenames."
    )
    argsp.add_argument(
        '--start-date', '-s',
        required=False,
        default=None,
        type=parse_date,
        metavar="YYYY-MM-DD",
        help="Include only activities in progress on or after this date."
    )
    argsp.add_argument(
        '--end-date', '-e',
        required=False,
        default=None,
        type=parse_date,
        metavar="YYYY-MM-DD",
        help="Include only activities in progress on or before this date."
    )
    argsp.add_argument(
        '--humanitarian-only', '-H',
        action='store_const',
        const=True,
        help="Include only activities with the IATI humanitarian marker."
    )
    argsp.add_argument(
        '--verbose', '-v',
        action='store_const',
        const=True,
        help="Print verbose debugging information to the console."
    )
    argsp.add_argument(
        '--quiet', '-q',
        action='store_const',
        const=True,
        help="No console output except error messages."
    )
    argsp.add_argument(
        'file_or_url',
        help="URL or local filename of an IATI activity file."
    )

    # Parse the command-line arguments
    args = argsp.parse_args()

    # Set up logging output
    if args.verbose: # -v
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet: # -q
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    # run the application
    split(
        args.file_or_url,
        args.max_activities,
        output_dir=args.output_directory,
        output_stub=args.output_stub,
        start_date=args.start_date,
        end_date=args.end_date,
        humanitarian_only=args.humanitarian_only
    )


def exec():
    """Entry function for setup.py script installation."""
    main(sys.argv)


if __name__ == '__main__':
    """Function for when module is invoked directly"""
    exec()

