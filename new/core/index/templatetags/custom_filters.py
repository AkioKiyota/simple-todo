from django import template

register = template.Library()

@register.filter
def is_instance_of(value, model_path):
    """check if given model is instance of given path"""
    return value.__class__.__module__ + '.' + value.__class__.__name__ == model_path
