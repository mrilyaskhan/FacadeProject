from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css):
    if isinstance(value, BoundField):
        return value.as_widget(attrs={"class": css})
    return value  