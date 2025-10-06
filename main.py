import argparse
import builder
import creator
import os

"""
Parse command line arguments.
"""
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Show verbose output.", action="store_true")
    commands = parser.add_mutually_exclusive_group()
    commands.add_argument("-b", "--build", metavar="<DIR>", help="Build a site in the specified directory. The site will be built to <DIR>/_site/")
    commands.add_argument("-n", "--new", metavar="<DIR>", help="Create a new blank site in the specified directory.")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.build:
        site_dir = args.build
        dest_dir = os.path.join(site_dir, "_site")
        builder.build_site(site_dir, dest_dir)

    if args.new:
        site_dir = args.new
        creator.create_new_site(site_dir)


if __name__ == "__main__":
    main()
