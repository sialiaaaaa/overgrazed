import markdown
import argparse
import os
import shutil
from pathlib import Path

md = markdown.Markdown(extensions=["meta", "footnotes"]) # Set up md with extensions


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
def format_template(site_dir, template, snippets):

    templates_dir = os.path.join(site_dir, "_templates")
    template_path = os.path.join(templates_dir, template + ".html")
    with open(template_path, "r") as f:
        template = f.read()

    for snippet_name in snippets:
        template = template.replace(snippet_name, snippets[snippet_name])
    formatted_template = template

    return formatted_template


"""
Converts Markdown to HTML. Returns both the HTML and a dict of the metadata.
"""
def convert_md_to_html(input_file):
    with open(input_file, "r") as f:
        md_content = f.read()

    md.reset()
    content = md.convert(md_content)
    meta = md.Meta

    return content, meta


"""
Build a page. First, get the converted content and metadata. Then determine which template the page wants to use.
Format the template, add the content to the template, and return it as text.
"""
def build_page(site_dir, page, snippets):
    content, meta = convert_md_to_html(page)
    template = format_template(site_dir, meta["template"][0], snippets)
    built_page = template.format(content=content)

    return built_page


"""
Build the site. First, copy everything except .md files and folders prefixed with '_' to the destination.
Then, iterate through the .md files and build them into pages.
"""
def build_site(site_dir, dest_dir, snippets):
    shutil.copytree(site_dir, dest_dir, ignore=shutil.ignore_patterns('*.md', '_*'), dirs_exist_ok=True) # Copy irrelevant files over.
    for filename in os.listdir(site_dir):
        if filename.endswith(".md" or ".markdown"):
            built_page = build_page(site_dir, os.path.join(site_dir, filename), snippets)
            new_filename = Path(filename).stem + ".html"
            with open(os.path.join(dest_dir, new_filename), "w") as f:
                f.write(built_page)


def main():
    args = parse_args()
    site_dir = args.input
    dest_dir = args.output

    snippets = get_snippets(site_dir)

    # page = build_page(site_dir, os.path.join(site_dir, "index.md"), snippets)

    # output_dir = dest_dir

    #if not os.path.exists(output_dir):
     #   os.makedirs(output_dir)

    #with open(os.path.join(dest_dir, "index.html"), "w") as f:
     #   f.write(page)

    build_site(site_dir, dest_dir, snippets)
    # format_template(site_dir, "global", snippets)
    #print(convert_md_to_html(os.path.join(site_dir, "index.md")))


if __name__ == "__main__":
    main()
