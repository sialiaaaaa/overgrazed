# About
There are a lot of static site generators. I know this because, frustrated with [Cobalt](https://cobalt-org.github.io/) and [Jekyll](https://jekyllrb.com/), I set about looking for alternatives. I found [many](https://github.com/myles/awesome-static-generators). Rather than weed through them looking for one that behaved the way I wanted it to, I decided to write my own. I assume this same reasoning is why there are so many.

# Guide
Create a folder for your site source files. Inside it, create directories called `_templates` and `_snippets`. In `_templates`, put HTML templates that you want your Markdown pages to use. Within the templates, you can refer to snippets by writing `%snippet_name%`. Also put `{content}` somewhere; this is where the Markdown-converted-to-HTML will go. In `_snippets`, put HTML files with bits of HTML you want to be able to insert into templates (header, footer, etc.).

Then, write Markdown files. The Markdown files will get converted into HTML and substituted for `{content}` in the relevant template.
