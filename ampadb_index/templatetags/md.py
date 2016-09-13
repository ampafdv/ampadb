from django import template
from django.utils.html import mark_safe
from ampadb_index.parse_md import parse_md

register = template.Library()

@register.filter
def md(text):
    return mark_safe(parse_md(text))

class MarkdownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        text = self.nodelist.render(context)
        return mark_safe(parse_md(text))

@register.tag(name="markdown")
def do_markdown(parser, token):
    nodelist = parser.parse(('endmarkdown'))
    parser.delete_first_token()
    return MarkdownNode(nodelist)
