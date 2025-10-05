import markdown as md
import argparse
import os
from pathlib import Path

"""
Parse command line arguments.
"""
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Show verbose output.", action="store_true")
    parser.add_argument("input", metavar="<INPUT>", help="Specify a site folder to build. Markdown files in this directory will be converted to HTML. Sub-directories starting with '-' will be skipped; all other files will be copied in-place.")
    parser.add_argument("output", metavar="<OUTPUT>", help="Specify a folder for the built site.")
    return parser.parse_args()


"""
Read the template directory and return a list of template strings.
"""
def get_templates(site_dir):

    # Get the directory to work with.
    templates_dir = os.path.join(site_dir, "_templates")

    # Create a list of templates (strings), prior to being formatted.
    templates = []
    for template_file in os.listdir(templates_dir):
        if template_file.endswith(".html"):
            template_path = os.path.join(templates_dir, template_file)
            with open(template_path, "r") as f:
                templates.append(f.read())

    return templates


"""
Create a dictionary of names of snippets and their content.
"""
def get_snippets(site_dir):

    # Get the directory to work with.
    snippets_dir = os.path.join(site_dir, "_snippets")

    snippets = {}
    for snippet_file in os.listdir(snippets_dir): # Loop through all the snippet files
        if snippet_file.endswith(".html"):
            snippet_path = os.path.join(snippets_dir, snippet_file)
            with open(snippet_path, "r") as f:
                snippets["%" + Path(snippet_path).stem + "%"] = f.read() # Set the dictionary keys to %[filename]%

    return snippets


"""
Takes a template (string) and dictionary of snippets and substitutes occurences of dict keys with the dict content.
"""
def format_template(template, snippets):

    for snippet_name in snippets:
        template = template.replace(snippet_name, snippets[snippet_name])
    formatted_template = template

    return formatted_template


def convert_md_to_html(input_file):
    with open(input_file, "r") as f:
        md_content = f.read()

    md.reset()
    content = md.convert(md_content)

    return content

def main():
    args = parse_args()
    site_dir = args.input
    dest_dir = args.output

    templates = get_templates(site_dir)
    snippets = get_snippets(site_dir)

    formatted_templates = []
    for template in templates:
        formatted_templates.append(format_template(template, snippets))

    print(formatted_templates)



if __name__ == "__main__":
    main()
