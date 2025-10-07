import markdown
import argparse
import os
import shutil
import builder
from validator import is_ignored_filename
from pathlib import Path

md = markdown.Markdown(extensions=["meta", "footnotes", "mdx_wikilink_plus"],
                       extension_configs={
                           "mdx_wikilink_plus": {"end_url": ".html", "url_whitespace": "-", "url_case": "lowercase"}
                           }
                       ) # Set up md with extensions

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
def format_template(site_dir, template):

    snippets = get_snippets(site_dir) # Get the dictionary of snippets

    templates_dir = os.path.join(site_dir, "_templates")
    template_path = os.path.join(templates_dir, template + ".html") # Open a template file and read it into a variable
    with open(template_path, "r") as f:
        template = f.read()

    for snippet_name in snippets:
        template = template.replace(snippet_name, snippets[snippet_name]) # Replace every instance of %snippet_name% with the content of the snippet
    formatted_template = template

    return formatted_template


"""
Converts Markdown to HTML. Returns both the HTML and a dict of the metadata.
"""
def convert_md_to_html(input_file):
    with open(input_file, "r") as f: # Read the content of a Markdown file into a variable
        md_content = f.read()

    md.reset()
    content = md.convert(md_content) # Convert the Markdown to HTML and store the output
    meta = md.Meta # Store the metadata too!

    return content, meta


"""
Build a page. First, get the converted content and metadata. Then determine which template the page wants to use.
Format the template, add the content to the template, and return it as text.
"""
def build_page(site_dir, page):
    content, meta = convert_md_to_html(page) # Get the page content and metadata
    template = format_template(site_dir, meta["template"][0]) # Use the metadata to figure out which template to use, then format that template
    built_page = template.format(content=content) # Apply the content to the formatted template

    return built_page


"""
Build the site. First, copy everything except .md files and folders prefixed with '_' or '.' to the destination.
Then, iterate through the .md files and build them into pages.
"""
def build_site(site_dir, dest_dir):
    shutil.copytree(
        site_dir,
        dest_dir,
        ignore=lambda directory, contents: {name for name in contents if is_ignored_filename(name)}.union({name for name in contents if name.endswith('.md') or name.startswith('_')}),
        dirs_exist_ok=True) # Copy irrelevant files over

    for root, dirs, files in os.walk(site_dir): # Walk the site directory searching for Markdown files
        for filename in files:
            if filename.endswith(".md"):
                current_file_path = root.replace(site_dir, "")
                built_page = build_page(site_dir, os.path.join(site_dir, current_file_path, filename)) # Build the Markdown files into pages
                new_filename = Path(filename).stem + ".html"
                with open(os.path.join(dest_dir, current_file_path, new_filename), "w") as f: # Write the built pages into the same location at the destination
                    f.write(built_page)
