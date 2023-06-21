import argparse
from .DatasetConverter import DatasetConverter
from .PathUtil import fixPath

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdir', type=str, required=True)
    parser.add_argument('--ddir', type=str, required=True)
    parser.add_argument('--iw', type=str, required=True)
    parser.add_argument('--ow', type=str, required=True)
    parser.add_argument('--classes', type=str, required=False, nargs='+')
    args = parser.parse_args()
    sdir = fixPath(args.sdir)
    ddir = fixPath(args.ddir)
    iw = args.iw
    ow = args.ow
    classes = args.classes
    converter = DatasetConverter()
    converter.convert(sdir, ddir, iw, ow, classes)

if __name__ == "__main__":
    main()