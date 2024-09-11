from django import template

register = template.Library()


@register.simple_tag
def img_tag(data):
    if data:
        return f'/media/{data}'
    return "#"
