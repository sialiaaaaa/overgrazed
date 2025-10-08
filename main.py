from pathlib import Path
import argparse
import sys

import builder
import creator
import server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="show verbose output", action="store_true") # Not in use
    commands = parser.add_mutually_exclusive_group()
    commands.add_argument("-b", "--build", action="store_true", help="build a site in the specified directory. The site will be built to <DIR>/_site/")
    commands.add_argument("-n", "--new", action="store_true", help="create a new blank site in the specified directory")
    commands.add_argument("-s", "--serve", action="store_true", help="repeatedly build and serve a site in the specified directory")
    parser.add_argument("-p", "--port", metavar="<PORT>", help="specify a port to serve the site (when using -s)")
    parser.add_argument("path", metavar="<DIR>")

    args = parser.parse_args()

    site_path = Path(args.path).resolve()
    dest_path = (site_path / "_site").resolve()

    if args.build:
        try:
            builder.build_site(site_path, dest_path) # Build the site once to start
            print(f"Built site to {dest_path}")
        except Exception as e:
            print(f"Failed to build site: {e}")

    if args.serve:
        port = int(args.port) if args.port else 1814
        server.serve_site(site_path, dest_path, port) # If the --serve option was chosen, call the server

    if args.new:
        creator.create_new_site(site_path) # If the --new option was chosen, attempt to create a site at the destination


if __name__ == "__main__":
    main()
