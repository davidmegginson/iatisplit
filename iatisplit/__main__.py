from iatisplit.split import run
import sys, argparse, logging

logger = logging.getLogger(__name__)

def main(args):

    def parse_date(s):
        if re.match('^\d{4}-\d{2}-\d{2}$', s):
            return s
        else:
            raise Exception("Bad date format: {}".format(s))

    logging.basicConfig(level=logging.INFO)
    
    argsp = argparse.ArgumentParser(description="Split IATI activity files.")
    argsp.add_argument(
        '--max-activities', '-n',
        required=True,
        type=int,
        metavar="NUMBER",
        help="Maximum number of IATI activities to include in each output file."
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
        'file_or_url',
        help="URL or local filename of an IATI activity file."
    )
    args = argsp.parse_args()
    run(args.file_or_url, args.max_activities, ".", args.start_date, args.end_date, args.humanitarian_only)

def exec():
    main(sys.argv)

if __name__ == '__main__':
    exec()

