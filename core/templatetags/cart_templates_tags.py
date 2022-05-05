from django import template
from core.models import *
from django.core.exceptions import ObjectDoesNotExist


register = template.Library()

@register.simple_tag
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.inclusion_tag('cart.html')
def show_results(user):
    try:
      order = Order.objects.get(user=user,ordered=False)
      order_items = order.items

      context = {"order_items":order_items,"order":order,}
    except ObjectDoesNotExist:

      context={}

    return context

@register.inclusion_tag('nav.html')
def navbar():
    try:
      category = Category.objects.all()


      context = {"category":category}
    except ObjectDoesNotExist:

      context={}

    return context

# def check_cart(pk):
#     check = False
#     try:
#         item_id = get_object_or_404()
#         order = Order.objects.get(user=user,ordered=False)
#         order_items = order.items
#
#         if item_id in order_item:
#             check = True
#
#     except ObjectDoesNotExist:
#         check = False
#
#     return check
