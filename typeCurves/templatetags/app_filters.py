from django import template

register = template.Library()

@register.filter(name = 'customRound')
def customRound(value):
	return round(value, 2)