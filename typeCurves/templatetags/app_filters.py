from django import template

register = template.Library()

@register.filter(name = 'customRound')
def customRound(value):
	return round(value, 2)


@register.filter(name = 'changeDate')
def changeDate(value):
	return value.strftime('%m/%d/%Y')