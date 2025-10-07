import os
import sys
import shutil
import tempfile


"""
Generates the model template into a supplied directory
"""
def generate_template(template_dir):
    with open(os.path.join(template_dir, "default.html"), "w") as f: # Write the default template
        f.write("""<!DOCTYPE html>
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


"""
Generates the model snippets into a supplied directory
"""
def generate_snippets(snippets_dir):
    with open(os.path.join(snippets_dir, "head.html"), "w") as f: # Write the default head snippet
        f.write("""<meta charset="utf-8">
<link rel="stylesheet" href="styles.css">
<title>My Website</title>""")

    with open(os.path.join(snippets_dir, "header.html"), "w") as f: # Write the default header snippet
        f.write("""<h1>My Website Header</h1>""")

    with open(os.path.join(snippets_dir, "footer.html"), "w") as f: # Write the default footer snippet
        f.write("""<p>My Website Footer</p>""")


"""
Generates the model index into a supplied directory
"""
def generate_index(directory):
    with open(os.path.join(directory, "index.md"), "w") as f: # Write the default index page
        f.write("""template: default

# Welcome to your new site!

Try editing this page or creating some more!""")


"""
Generates a blank css file into a supplied directory
"""
def generate_css(directory):
    with open(os.path.join(directory, "styles.css"), "w") as f: # Create an empty styles.css
        f.write("")


"""
Finds an appropriate temp directory to create the site, then
basically just calls the above functions, with some checks and error handling.
Finally, copies the site atomically to the target destination.
"""
def create_new_site(directory):
    root = os.path.join(tempfile.gettempdir(), os.path.basename(os.path.normpath(directory))) # Find the system temp directory and use it as the site root
    shutil.rmtree(root, ignore_errors=True) # Delete anything already in the temporary root

    template_dir = os.path.join(root, "_templates") # Get some other useful paths
    snippets_dir = os.path.join(root, "_snippets")

    try:
        os.makedirs(root)
        os.makedirs(template_dir)
        os.makedirs(snippets_dir) # Try to create the directories
    except Exception as e:
        print(f"Could not create one or more directories.\n{e}\n\nNo files were created. Exiting...")
        shutil.rmtree(root) # Delete the temporary files if there's an error (redundant, but practical)
        sys.exit()

    generate_template(template_dir)
    generate_snippets(snippets_dir)
    generate_index(root)
    generate_css(root) # Call each generate function

    try:
        shutil.copytree(root, directory) # Copy the entire site atomically from the temp directory to the target
    except Exception as e:
        print(f"Could not create site at {directory}.\n{e}\n\nNo files were created. Exiting...")
        shutil.rmtree(root) # Same cleanup process as above
        sys.exit()

    print(f"Created a new blank site at {directory}!")


