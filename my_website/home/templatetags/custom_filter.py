# from django import template
#
# register = template.Library()
#
# @register.filter(name='currency')
# def currency(number):
#     return "VNĐ "+str(number)
#
#
#
# @register.filter(name='multiply')
# def multiply(number , number1):
#     return number * number1

from django import template

register = template.Library()

@register.filter
def format_currency(value):
    """
    Định dạng giá tiền thành chuỗi có dấu chấm phân cách hàng nghìn.
    """
    try:
        value = int(value)
        return f"{value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value


