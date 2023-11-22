import sys
from drug_finder.motor import Motor

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    drugfinder = Motor()
    drugfinder.welcome()

if __name__ == '__main__':
    sys.exit(main())