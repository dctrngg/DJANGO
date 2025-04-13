
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from home.models.product import Products
from home.models.category import Category
from django.views import View
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.shortcuts import render
from ..models.product import Products

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    text = str(request.POST.get('search')).strip()
    if text != 'None':
        products = Products.get_products_by_text(text)
    else:
        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            products = Products.get_all_products()
    data = {}
    data['categories'] = categories

    # Lấy các sản phẩm tương ứng dựa vào phân trang

    # Paginate Items
    items_per_page = 15
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['products'] = page_obj
    return render(request, 'index.html', data)

def search(request):
    query = request.GET.get('q')
    if query:
        products = Products.objects.filter(name__icontains=query) # Tìm kiếm theo tên sản phẩm
    else:
        products = Products.objects.none() # Không có sản phẩm nào nếu không có truy vấn

    return render(request, 'index.html', {'products': products})

def product_list(request):
    sort_by = request.GET.get('sort', 'name') # Mặc định sắp xếp theo tên
    if sort_by == 'price':
        products = Products.objects.all().order_by('price')
    else:
        products = Products.objects.all().order_by('name')
    return render(request, 'index.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    product = get_object_or_404(Products, id=product_id)
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1
        }
    request.session['cart'] = cart
    previous_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(previous_url)

def cart_view(request):
    cart = request.session.get('cart', {})
    total_price = 0
    for product_id, item in cart.items():
        if isinstance(item, dict):
            item['total_price'] = item.get('price', 0) * item.get('quantity', 1)
            total_price += item['total_price']
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)] 
    request.session['cart'] = cart
    previous_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(previous_url)

def update_cart_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        quantity = request.POST.get('quantity')
        if quantity.isdigit() and int(quantity) > 0:
            cart[str(product_id)]['quantity'] = int(quantity) 
        else:
            del cart[str(product_id)] 
    request.session['cart'] = cart
    previous_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(previous_url)

# -------------------------------SHIPPING------------------------------------

from django.shortcuts import render, redirect

from home.models.shippingaddress import ShippingAddress, Order
from django.contrib.auth.decorators import login_required

def calculate_shipping_cost(cart_total, address):
    
    
        if cart_total > 500000:  
            return 0
        else:
            return 50000  
        
# --------------------------------------------------
from django.shortcuts import redirect, render
from django.contrib import messages


@login_required
def create_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'Giỏ hàng của bạn đang trống. Vui lòng chọn sản phẩm.')
        return redirect('cart_view')

    if request.method == 'POST':
        # Lấy dữ liệu từ POST
        address_line_1 = request.POST.get('address_line_1')
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city')
        state = request.POST.get('state')

        # Kiểm tra email
        if not email:
            messages.error(request, 'Email không được để trống.')
            return redirect('create_order')

        if not address_line_1 or not city or not state:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin địa chỉ.')
            return redirect('create_order')

        # Tạo đối tượng ShippingAddress
        shipping_address = ShippingAddress.objects.create(
            user=request.user,
            address_line_1=address_line_1,
            email=email,
            city=city,
            state=state
        )

        # Tính tổng giá trị đơn hàng
        cart_total = sum(item['price'] * item['quantity'] for item in cart.values())

        # Tính phí vận chuyển
        shipping_cost = calculate_shipping_cost(cart_total, shipping_address)

        # Tạo đơn hàng
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            total_amount=cart_total,
            shipping_cost=shipping_cost
        )

        # Gửi email xác nhận với chi tiết giỏ hàng
        order_details = {
            'shipping_cost': shipping_cost
        }
        send_confirmation_email(email, cart, order_details)

        # Dọn dẹp giỏ hàng
        request.session['cart'] = {}

        messages.success(request, 'Đơn hàng của bạn đã được xác nhận. Cảm ơn bạn!')
        return redirect('order_success', order_id=order.id)

    return render(request, 'cart.html')



#  --------------------
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)  
    return render(request, 'order_success.html', {'order': order})

#  -------------------------------

import logging

logger = logging.getLogger(__name__)

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def send_confirmation_email(email, cart, order_details):
    # Tạo phần nội dung cho từng sản phẩm
    order_items_html = ""
    total_price = 0

    for product_id, item in cart.items():
        product_name = item['name']
        quantity = item['quantity']
        price = item['price']
        total_item_price = price * quantity
        total_price += total_item_price

        order_items_html += f"""
        <tr>
            <td style="padding: 10px;">{product_name}</td>
            <td style="padding: 10px;">{quantity}</td>
            <td style="padding: 10px;">{price:,} VND</td>
            <td style="padding: 10px;">{total_item_price:,} VND</td>
        </tr>
        """

    shipping_cost = order_details.get('shipping_cost', 0)
    total_payment = total_price + shipping_cost
    tracking_url = order_details.get('tracking_url', '#')

    # HTML template email
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <div style="background-color: #2c3e50; padding: 20px; text-align: center;">
                <img src="https://yourstore.com/logo.png" alt="Điện thoại XYZ" style="max-height: 50px;" />
            </div>
            <div style="padding: 20px;">
                <h2 style="color: #333;">Cảm ơn bạn đã đặt hàng tại <span style="color: #2980b9;">Điện thoại XYZ</span>!</h2>
                <p style="color: #555;">Chúng tôi đã nhận được đơn hàng của bạn. Dưới đây là thông tin chi tiết:</p>
                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <thead>
                        <tr style="background-color: #ecf0f1; text-align: left;">
                            <th style="padding: 10px;">Sản phẩm</th>
                            <th style="padding: 10px;">Số lượng</th>
                            <th style="padding: 10px;">Giá</th>
                            <th style="padding: 10px;">Tổng</th>
                        </tr>
                    </thead>
                    <tbody>
                        {order_items_html}
                    </tbody>
                </table>
                <div style="margin-top: 20px; font-size: 16px; color: #333;">
                    <p><strong>Tổng giá trị đơn hàng:</strong> {total_price:,} VND</p>
                    <p><strong>Phí vận chuyển:</strong> {shipping_cost:,} VND</p>
                    <p style="font-size: 18px;"><strong>Tổng thanh toán:</strong> <span style="color: #e74c3c;">{total_payment:,} VND</span></p>
                </div>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{tracking_url}" style="background-color: #27ae60; color: white; padding: 12px 25px; text-decoration: none; border-radius: 4px;">Theo dõi đơn hàng</a>
                </div>
                <div style="margin-top: 30px; color: #999; font-size: 12px; text-align: center;">
                    <p>Điện thoại XYZ - Luôn đồng hành cùng bạn</p>
                    <p>Website: <a href="https://yourstore.com" style="color: #2980b9;">yourstore.com</a></p>
                    <p>Hotline: 0909 000 111</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Plain text fallback
    text_content = strip_tags(html_content)

    try:
        msg = EmailMultiAlternatives(
            subject='Xác nhận đơn hàng – Điện thoại XYZ',
            body=text_content,
            from_email='ductrungnguyen30@gmail.com',
            to=[email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info(f'Email đã được gửi đến: {email}')
    except Exception as e:
        logger.error(f'Không thể gửi email đến {email}: {e}')
