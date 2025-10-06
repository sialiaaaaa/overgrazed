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

# Frequently asked questions

***Why?*** I originally was trying to make my [very simple website](sialia.dev) with [Cobalt](https://cobalt-org.github.io/). It worked well enough, but for certain implementations I was frustrated with the lack of control I had over its inner workings. Looking for alternatives, I found [too many](https://github.com/myles/awesome-static-generators); rather than weed through all of these looking for one that behaved the way I wanted, I decided to write my own. I suspect this reasoning is why there are so many.

***No, I mean, why the name?*** Because the idea and a lot of the implementation are thanks to [Cosmo](https://cosmo.tardis.ac/). "Overgrazed" references the [Tragedy of the commons](https://en.wikipedia.org/wiki/Tragedy_of_the_commons), where someone takes advantage of a shared resource; in this case, Cosmo's willingness to send me their script for converting Markdown into HTML.
