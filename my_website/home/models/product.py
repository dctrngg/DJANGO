# from django.db import models
# from .category import Category
# from ckeditor.fields import RichTextField
#
# class Products(models.Model):
#     name = models.CharField(max_length=60)
#     price = models.IntegerField(default=0)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
#     description = RichTextField(default='', blank=True, null=True)
#     image = models.ImageField(upload_to='uploads/products/')
#
#     def __str__(self):
#         return self.name
#
#     @staticmethod
#     def get_product_by_id(ids):
#         return Products.objects.filter(id=ids)
#
#     @staticmethod
#     def get_products_by_id(ids):
#         return Products.objects.filter(id__in=ids)
#
#     @staticmethod
#     def get_all_products():
#         return Products.objects.all()
#
#     @staticmethod
#     def get_all_products_by_categoryid(category_id):
#         if category_id:
#             return Products.objects.filter(category=category_id)
#         else:
#             return Products.get_all_products()
#
#     @staticmethod
#     def get_products_by_text(text):
#         return Products.objects.filter(name__icontains=text)
#
# class ProductImage(models.Model):
#     product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='uploads/products/')
#     is_featured = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Image for {self.product.name}"
#
#     @staticmethod
#     def get_featured_image(product_id):
#         return ProductImage.objects.filter(product_id=product_id, is_featured=True).first()
#
#     @staticmethod
#     def get_all_images_by_product(product_id):
#         return ProductImage.objects.filter(product_id=product_id)

from django.db import models
from .category import Category
from ckeditor.fields import RichTextField
from django.db.models import Q

class MyModel(models.Model):
    price = models.IntegerField(default=0)

class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)  # Thêm trường price vào Products
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = RichTextField(default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')

    def __str__(self):
        return self.name

    @property
    def formatted_price(self):
        # Định dạng giá trị price thành chuỗi có dấu chấm
        return f"{self.price:,}".replace(',', '.')

    @staticmethod
    def get_product_by_id(ids):
        return Products.objects.filter(id=ids)

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()

    @staticmethod
    def get_products_by_text(text):
        return Products.objects.filter(name__icontains=text)

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/products/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"

    @staticmethod
    def get_featured_image(product_id):
        return ProductImage.objects.filter(product_id=product_id, is_featured=True).first()

    @staticmethod
    def get_all_images_by_product(product_id):
        return ProductImage.objects.filter(product_id=product_id)