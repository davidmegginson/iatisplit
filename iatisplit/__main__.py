from split import run
import sys, argparse

def main(args):

    def parse_date(s):
        if re.match('^\d{4}-\d{2}-\d{2}$', s):
            return s
        else:
            raise Exception("Bad date format: {}".format(s))
    
    argsp = argparse.ArgumentParser(description="Split IATI activity files.")
    argsp.add_argument('--max-activities', '-n', required=True, type=int)
    argsp.add_argument('--start-date', '-s', required=False, default=None, type=parse_date)
    argsp.add_argument('--end-date', '-e', required=False, default=None, type=parse_date)
    argsp.add_argument('--humanitarian-only', '-H', required=False, default=False, type=bool)
    argsp.add_argument('file_or_url', nargs='?')
    args = argsp.parse_args()
    run(args.file_or_url, args.max_activities, None, args.start_date, args.end_date, args.humanitarian_only)
    

if __name__ == '__main__':
    main(sys.argv)

