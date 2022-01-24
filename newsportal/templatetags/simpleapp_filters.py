from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value, arg):
    value = value.replace("жесть", "ЗДОРОВО")
    value = value.replace("афигенно", "ЗДОРОВО")
    value = value.replace("круто", "ЗДОРОВО")
    return value




@register.filter(name='Censor1')
def Censor1(value, arg):

    if ("жесть" in value) or ("афигенно" in value) or ("круто" in value):
        arg = 'ВНИМАНИЕ, ВНИМАНИЕ!!! Говорит BBC!!! В тексте используется ненормативная лексика, применен цензуру (замена слов)'
        return arg
    else:
        return value