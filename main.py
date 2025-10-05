import markdown as md
import argparse
import os

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Show verbose output.", action="store_true")
    parser.add_argument("input", metavar="<INPUT>", help="Specify a site folder to build. Markdown files in this directory will be converted to HTML. Sub-directories starting with '-' will be skipped; all other files will be copied in-place.")
    parser.add_argument("output", metavar="<OUTPUT>", help="Specify a folder for the built site.")
    return parser.parse_args()

def main():
    args = setup_args()
    print(os.listdir(args.input))

if __name__ == "__main__":
    main()
