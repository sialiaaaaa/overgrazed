import argparse
import builder
import creator
import server
import os
import sys


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="show verbose output", action="store_true") # Not in use
    commands = parser.add_mutually_exclusive_group()
    commands.add_argument("-b", "--build", metavar="<DIR>", help="build a site in the specified directory. The site will be built to <DIR>/_site/")
    commands.add_argument("-n", "--new", metavar="<DIR>", help="create a new blank site in the specified directory")
    commands.add_argument("-s", "--serve", metavar="<DIR>", help="repeatedly build and serve a site in the specified directorye")
    return parser.parse_args()


def main():

    args = parse_args() # Create an instance of the args

    if args.build:
        site_dir = args.build
        dest_dir = os.path.join(site_dir, "_site")
        try:
            builder.build_site(site_dir, dest_dir) # Build the site once to start
            print(f"Built site to {dest_dir}")
        except Exception as e:
            print(f"Failed to build site: {e}")

    if args.serve:
        site_dir = args.serve
        dest_dir = os.path.join(site_dir, "_site")
        port = 1814

        server.serve_site(site_dir, dest_dir, port) # If the --serve option was chosen, call the server

    if args.new:
        site_dir = args.new
        if os.path.isdir(site_dir): # Check if the supplied folder exists, since this would cause an error anyway
            print(f"A folder already exists at {site_dir}. No files were created. Exiting...")
            sys.exit()
        creator.create_new_site(site_dir) # If the --new option was chosen, attempt to create a site at the destination


if __name__ == "__main__":
    main()
