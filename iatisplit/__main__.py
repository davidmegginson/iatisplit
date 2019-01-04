from iatisplit.split import split
from iatisplit.version import __version__
import re, sys, argparse, logging

logger = logging.getLogger(__name__)
"""Logger for this module"""


def main(args):
    """Entry point for a script.
    Note that argparse expects the script name (sys.args[0]) to be removed,
    so provide only the args themselves, not the traditional ARGV[0].
    @args: a list of command-line arguments
    """
    
    def parse_date(s):
        """Make sure we have an ISO YYYY-MM-DD date"""
        if re.match('^\d{4}-\d{2}-\d{2}$', s):
            return s
        else:
            raise Exception("Bad date format: {}".format(s))

    parser = argparse.ArgumentParser(description="Split IATI activity files.")
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__)
    )
    parser.add_argument(
        '--max-activities', '-n',
        required=True,
        type=int,
        metavar="NUMBER",
        help="Maximum number of IATI activities to include in each output file."
    )
    parser.add_argument(
        '--output-directory', '-d',
        required=False,
        default=".",
        metavar="path/to/output/directory",
        help="Put output files in this directory (instead of the current one)."
    )
    parser.add_argument(
        '--output-stub', '-o',
        required=False,
        default=None,
        metavar="filename",
        help="Stub for creating output filenames."
    )
    parser.add_argument(
        '--start-date', '-s',
        required=False,
        default=None,
        type=parse_date,
        metavar="YYYY-MM-DD",
        help="Include only activities in progress on or after this date."
    )
    parser.add_argument(
        '--end-date', '-e',
        required=False,
        default=None,
        type=parse_date,
        metavar="YYYY-MM-DD",
        help="Include only activities in progress on or before this date."
    )
    parser.add_argument(
        '--transaction-type',
        required=False,
        default=None,
        metavar="<IATI transaction type",
        help="Include only activities with a transaction of this type."
    )
    parser.add_argument(
        '--transaction-start-date',
        required=False,
        default=None,
        type=parse_date,
        metavar="YYYY-MM-DD",
        help="Include only activities in progress on or after this date."
    )
    parser.add_argument(
        '--transaction-end-date',
        required=False,
        default=None,
        type=parse_date,
        metavar="YYYY-MM-DD",
        help="Include only activities in progress on or before this date."
    )
    parser.add_argument(
        '--humanitarian-only', '-H',
        action='store_const',
        const=True,
        help="Include only activities with the IATI humanitarian marker."
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_const',
        const=True,
        help="Print verbose debugging information to the console."
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_const',
        const=True,
        help="No console output except error messages."
    )
    parser.add_argument(
        'file_or_url',
        help="URL or local filename of an IATI activity file."
    )

    # Parse the command-line arguments
    result = parser.parse_args(args)

    # Set up logging output
    if result.verbose: # -v
        logging.basicConfig(level=logging.DEBUG)
    elif result.quiet: # -q
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    # run the application
    split(
        result.file_or_url,
        result.max_activities,
        output_dir=result.output_directory,
        output_stub=result.output_stub,
        start_date=result.start_date,
        end_date=result.end_date,
        humanitarian_only=result.humanitarian_only,
        transaction_type=result.transaction_type,
        transaction_start_date=result.transaction_start_date,
        transaction_end_date=result.transaction_end_date
    )


def exec():
    """Entry function for setup.py script installation."""
    main(sys.argv[1:])


if __name__ == '__main__':
    """Function for when module is invoked directly"""
    exec()

