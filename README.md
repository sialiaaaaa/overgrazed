# About
There are a lot of static site generators. I know this because, frustrated with [Cobalt](https://cobalt-org.github.io/) and [Jekyll](https://jekyllrb.com/), I set about looking for alternatives. I found [many](https://github.com/myles/awesome-static-generators). Rather than weed through them looking for one that behaved the way I wanted it to, I decided to write my own. I assume this same reasoning is why there are so many.

# Documentation

## Quickstart guide

Use the `-n` option to create a new blank site in a directory. Amend the generated templates and snippets as desired (or create your own!) and write CSS and Markdown in the files provided. You can make as many Markdown pages as you like, linking between them with WikiLinks syntax (see below).

When you're ready to see your site, use the `-b` option. This will build the site into `_site`. You can preview the site by opening `_site/index.html` in a browser of your choice.

## Templates and snippets

**Templates** are bits of HTML stored as files in `_templates`. A template is the HTMl that a page's content will be wrapped in when the site is built. Each page must have a template specified in its frontmatter (see below).

Templates can make reference to **snippets**, even smaller bits of HTML you might want to repeat across multiple templates. Snippets are stored in `_snippets` and can be referenced within templates by writing `%<snippet name>%`.

## Frontmatter

Each page (a `.md` file) should have **frontmatter**; effectively metadata for that page. Currently, Overgrazed supports only the `template` option, which is required by every page and determines which template to insert that page's content into.

## WikiLinks

Overgrazed has support for [WikiLinks](https://en.wikipedia.org/wiki/Wiki#Linking_to_and_naming_pages) style linking. Specifically, links like `[[path/to/page name]]` will link to files on your site.
