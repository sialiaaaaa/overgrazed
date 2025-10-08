from pathlib import Path
import sys
import shutil
import tempfile



def generate_template(template_dir):
    """
    Generates the model template into a supplied directory
    """

    (template_dir / "default.html").write_text("""<!DOCTYPE html>
<html lang="">
    <head>
        %head%
    </head>
    <body>
        <header>
            %header%
        </header>
        <main>
            {content}
        </main>
        <footer>
            %footer%
        </footer>
    </body>
</html>""")


def generate_snippets(snippets_dir):
    """
    Generates the model snippets into a supplied directory
    """
    (snippets_dir / "head.html").write_text("""<meta charset="utf-8">
<link rel="stylesheet" href="styles.css">
<title>My Website</title>""")

    (snippets_dir / "header.html").write_text("""<h1>My Website Header</h1>""")
    (snippets_dir / "footer.html").write_text("""<p>My Website Footer</p>""")


def generate_index(directory):
    """
    Generates the model index into a supplied directory
    """
    (directory / "index.md").write_text("""template: default

# Welcome to your new site!

Try editing this page or creating some more!""")


def generate_css(directory):
    """
    Generates a blank css file into a supplied directory
    """
    (directory / "styles.css").write_text("")


def create_new_site(directory):
    """
    Finds an appropriate temp directory to create the site, then
    basically just calls the above functions, with some checks and error handling.
    Finally, copies the site atomically to the target destination.
    """
    directory = directory.resolve()

    # Check if directory already exists
    if directory.exists():
        print(f"A folder already exists at {directory}. No files were created. Exiting...")
        sys.exit()

    root = Path(tempfile.gettempdir()) / f"overgrazed_{directory.name}" # Find the system temp directory and use it as the site root
    if root.exists():
        print(f"Warning: Temporary directory {root} exists. Removing...")
    shutil.rmtree(root, ignore_errors=True) # Delete anything already in the temporary root

    template_dir = root / "_templates" # Get some other useful paths
    snippets_dir = root / "_snippets"

    try:
        root.mkdir(parents=True, exist_ok=True)
        template_dir.mkdir()
        snippets_dir.mkdir()
    except Exception as e:
        print(f"Could not create one or more directories.\n{e}\n\nNo files were created. Exiting...")
        shutil.rmtree(root, ignore_errors=True) # Delete the temporary files if there's an error (redundant, but practical)
        sys.exit()

    generate_template(template_dir)
    generate_snippets(snippets_dir)
    generate_index(root)
    generate_css(root) # Call each generate function

    try:
        shutil.copytree(root, directory) # Copy the entire site atomically from the temp directory to the target
    except Exception as e:
        print(f"Could not create site at {directory}.\n{e}\n\nNo files were created. Exiting...")
        shutil.rmtree(root, ignore_errors=True) # Same cleanup process as above
        sys.exit()

    print(f"Created a new blank site at {directory}!")


