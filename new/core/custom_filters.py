from django import template

register = template.Library()

@register.filter
def instance_of(value, model_path):
    return value.__class__.__module__ + '.' + value.__class__.__name__ == model_path
