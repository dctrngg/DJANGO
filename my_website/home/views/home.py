# from django.shortcuts import render , redirect , HttpResponseRedirect
# from home.models.product import Products, ProductImage
# from home.models.category import Category
# from home.models.customer import Customer
#
#
# from django.views import View
# from django.core.paginator import (
#     Paginator,
#     EmptyPage,
#     PageNotAnInteger,
# )
# def store(request):
#     cart = request.session.get('cart')
#     if not cart:
#         request.session['cart'] = {}
#     product = None
#     categories = Category.get_all_categories()
#     print('categories>>', categories)
#     categoryID = request.GET.get('category')
#     text = str(request.POST.get('search')).strip()
#     if text != 'None':
#         products = Products.get_products_by_tex(text)
#     else:
#         if categoryID:
#             products = Products.get_all_products_by_category(categoryID)
#         else:
#             products = Products.get_all_products()
#     data = {}
#     data['categories'] = categories
#
#     items_per_page = 12
#     paginator = Paginator(products, items_per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     data['products'] = page_obj
#     return render(request, 'store.html', data)
#
# class Detail(View):
#     def get(self, request):
#         ids = request.GET.get('product')
#         product = Products.get_products_by_id(ids)
#         product_images = ProductImage.get_all_images_by_product(ids)
#
#         main_image = str(product[0].image)
#
#         image_list = [main_image] + [str(image.image) for image in product_images]
#         context = {
#             'product': product[0],
#             'product_images': product_images,
#             'image_list': image_list,
#         }
#         return render(request, 'product-detail.html', context)
#
#     def post(self, request):
#         product = request.POST.get('product')
#         try:
#             quantity = int(request.POST.get('quantity'))
#         except:
#             pass
#         cart = request.session.get('cart')
#         postcmt = request.POST.get('postcmt')
#         customer = request.session.get('customer')
#         try:
#             if cart:
#
#                 genquantity = cart.get(product)
#                 if genquantity:
#                     cart[product] = genquantity + quantity
#             else:
#                 cart[product] = quantity
#         except:
#             pass
#         print('cart>>>', cart);
#         cmtid = request.POST.get('cmtid')
#         if str(postcmt) != 'None':
#             postcomment = Comment(content=postcmt,
#                                   date=date.today(),
#                                   product=Products(id=cmtid),
#                                   customer=Customer(id=customer))
#             postcomment.save()
#
#         request.session['cart'] = cart
#         return HttpResponseRedirect(f'/{request.get_full_path()[1:]}')
#
# class Index(View):
#     def get(self, request):
#         return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
#
#     def post(self, request):
#         product = request.POST.get('product')
#         remove = request.POST.get('remove')
#         cart = request.session.get('cart')
#         if cart:
#             quantity = cart.get(product)
#             if quantity:
#                 if remove:
#                     if quantity <= 1:
#                         cart.pop(product)
#                     else:
#                         cart[product] = quantity - 1
#                 else:
#                     cart[product] = quantity + 1
#
#             else:
#                 cart[product] = 1
#         else:
#             cart = {}
#             cart[product] = 1
#
#         request.session['cart'] = cart
#         print('cart', request.session['cart'])
#         return redirect('homepage')


from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from home.models.product import Products, ProductImage
from home.models.category import Category
from home.models.customer import Customer


from django.views import View
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

from home.models.comment import Comment
from home.models.form import CommentForm
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

class Detail(View):
    def get(self, request):
        product_id = request.GET.get('product')

        
        product = get_object_or_404(Products, id=product_id)

        
        product_images = ProductImage.get_all_images_by_product(product_id)

        
        main_image = str(product.image) if product.image else "default_image_url"
        image_list = [main_image] + [str(image.image) for image in product_images]

    
        comments = product.comments.all() 

        form = CommentForm()

        context = {
            'product': product,
            'product_images': product_images,
            'image_list': image_list,
            'comments': comments,
            'form': form,
        }

        return render(request, 'product-detail.html', context)

    def post(self, request):
        product_id = request.POST.get('product')  
        product = get_object_or_404(Products, id=product_id)

      
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user if request.user.is_authenticated else None  
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', 'store')) 

        product_images = ProductImage.get_all_images_by_product(product_id)
        main_image = str(product.image) if product.image else "default_image_url"
        image_list = [main_image] + [str(image.image) for image in product_images]
        comments = product.comments.all() 

        context = {
            'product': product,
            'product_images': product_images,
            'image_list': image_list,
            'comments': comments,
            'form': form,
        }

        return render(request, 'product-detail.html', context)

class Index(View):
    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')