from django import template
register = template.Library()

@register.filter
def sort_by(queryset, order):
    order = [seq.strip() for seq in order.split(',')]
    try:
        return queryset.order_by(order[0], order[1], order[2])
    except:
        try:
            return queryset.order_by(order[0], order[1])
        except:
            return queryset.order_by(order[0])
