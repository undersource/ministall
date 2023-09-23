from django import template
from shop.models import *
from shop.monero_rpc import *

register = template.Library()

@register.simple_tag(takes_context=True, name='balance')
def show_balance(context):
    index = context['request'].user.monero_account_index
    balance = get_balance(index)
    spent = context['request'].user.spent
    result = balance - spent

    return float(spent)

@register.inclusion_tag('shop/show_button.html', takes_context=True)
def show_button(context):
    purchases = context['request'].user.purchases.filter(slug=context['product'].slug)

    bought = True
    
    if purchases.count() == 0:
        bought = False

    return {'bought': bought, 'product': context['product']}

@register.filter()
def strip_zeros(num):
    numstr = str(num)
    numstrlen = len(numstr) - 1

    for i in range(numstrlen):
        if numstr[numstrlen - i] == '0':
            numstr.replace(numstr[numstrlen - i], '')
        else:
            return float(numstr)