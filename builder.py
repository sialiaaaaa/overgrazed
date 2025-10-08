from pathlib import Path
import markdown
import shutil
import sys

from validator import is_ignored_filename

md = markdown.Markdown(extensions=["meta", "footnotes", "mdx_wikilink_plus"],
                       extension_configs={
                           "mdx_wikilink_plus": {"end_url": ".html", "url_whitespace": "-", "url_case": "lowercase"}
                           }
                       ) # Set up md with extensions

def get_snippets(site_path):
    """
    Create a dictionary of names of snippets and their content.
    """

    # Get the directory to work with.
    snippets_dir = site_path / "_snippets"

    snippets = {}
    for snippet_file in snippets_dir.glob("*.html"): # Loop through all the snippet files
        snippets[f"%{snippet_file.stem}%"] = snippet_file.read_text() # Set the dictionary keys to %[filename]%

    return snippets


def format_template(site_path, template):
    """
    Takes a template (string) and dictionary of snippets and substitutes occurences of dict keys with the dict content.
    """

    snippets = get_snippets(site_path) # Get the dictionary of snippets

    template_path = site_path / "_templates" / f"{template}.html"

    if not template_path.exists():
        raise FileNotFoundError(f"\"{template}\" was not found in the _templates directory.")

    template_content = template_path.read_text()

    for snippet_name, snippet_content in snippets.items():
                template_content = template_content.replace(snippet_name, snippet_content) # Replace every instance of %snippet_name% with the content of the snippet

    return template_content


def convert_md_to_html(input_file):
    """
    Converts Markdown to HTML. Returns both the HTML and a dict of the metadata.
    """
    content = input_file.read_text()
    md.reset()
    html = md.convert(content) # Convert the Markdown to HTML and store the output
    return html, md.Meta

def build_page(site_path, page):
    """
    Build a page. First, get the converted content and metadata. Then determine which template the page wants to use.
    Format the template, add the content to the template, and return it as text.
    """

    content, meta = convert_md_to_html(page) # Get the page content and metadata
    if "template" in meta:
        template = format_template(site_path, meta["template"][0]) # Use the metadata to figure out which template to use, then format that template
    else:
        raise ValueError(f"No template frontmatter was provided for page \"{page}\"")


    built_page = template.format(content=content) # Apply the content to the formatted template

    return built_page


def build_site(site_path, dest_path):
    if not site_path.exists():
        print(f"Site directory {site_path} does not exist. No files were created. Exiting...")
        sys.exit()

    shutil.copytree(
        site_path,
        dest_path,
        ignore=lambda directory, contents: {
            name for name in contents
            if is_ignored_filename(name) or name.endswith('.md') or name.startswith('_')
        },
        dirs_exist_ok=True)

    for md_file in site_path.rglob("*.md"):
        if not is_ignored_filename(md_file.name):
            relative_path = md_file.relative_to(site_path)
            target_file = dest_path / relative_path.with_suffix('.html')

            target_file.parent.mkdir(parents=True, exist_ok=True)

            built_page = build_page(site_path, md_file)
            target_file.write_text(built_page)
