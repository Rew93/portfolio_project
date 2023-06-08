from django import template

register = template.Library()


@register.filter(name='range_number')
def range_number(number):
    return range(1, number+1)



