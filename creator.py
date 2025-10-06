import os
import shutil

def generate_template(template_dir):
    with open(os.path.join(template_dir, "default.html"), "w") as f:
        f.write("""
<!DOCTYPE html>
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
</html>
        """)

def generate_snippets(snippets_dir):
    with open(os.path.join(snippets_dir, "head.html"), "w") as f:
        f.write("""
<meta charset="utf-8">
<link rel="stylesheet" href="styles.css">
<title>My Website</title>
        """)

    with open(os.path.join(snippets_dir, "header.html"), "w") as f:
        f.write("""
<h1>My Website Header</h1>
        """)

    with open(os.path.join(snippets_dir, "footer.html"), "w") as f:
        f.write("""
<p>My Website Footer</p>
        """)

def generate_index(directory):
    with open(os.path.join(directory, "index.md"), "w") as f:
        f.write("""template: default

# Welcome to your new site!

Try editing this page or creating some more!
        """)

def generate_css(directory):
    with open(os.path.join(directory, "styles.css"), "w") as f:
        f.write("")

def create_new_site(directory):
    root = directory
    template_dir = os.path.join(root, "_templates")
    snippets_dir = os.path.join(root, "_snippets")
    os.makedirs(template_dir)
    os.makedirs(snippets_dir)

    generate_template(template_dir)
    generate_snippets(snippets_dir)
    generate_index(root)
    generate_css(root)

    print(f"Created a new blank site at {root}!")


