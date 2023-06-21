import argparse

from .DatasetConverter import DatasetConverter
from .PathUtil import fixPath

def main():
    parser = argparse.ArgumentParser(
        description="Converts all labels in a dataset from a specified format to another."
    )
    parser.add_argument('INPUT_PATH', type=str, help="input directory")
    parser.add_argument('OUTPUT_PATH', type=str, help="output directory")
    parser.add_argument('INPUT_WRAPPER', type=str, help="input wrapper")
    parser.add_argument('OUTPUT_WRAPPER', type=str, help="output wrapper")
    parser.add_argument(
        '--filter-classes',
        '-f',
        type=str,
        required=False,
        nargs='+',
        help="list of classes to be converted, all the other classes' bounding boxes will be ignored - default: filter disabled")
    parser.add_argument('--disable-copy', '-d', action='store_true', help='don\'t copy images to OUTPUT_PATH - default: copy enabled')
    args = parser.parse_args()
    in_dir = fixPath(args.INPUT_PATH)
    out_dir = fixPath(args.OUTPUT_PATH)
    in_wrap = args.INPUT_WRAPPER
    out_wrap = args.OUTPUT_WRAPPER
    classes = args.filter_classes
    copy = not args.disable_copy
    converter = DatasetConverter()
    converter.convert(
        in_dir, out_dir, in_wrap, out_wrap, classes, copy
    )

if __name__ == "__main__":
    main()