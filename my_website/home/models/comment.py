from django.db import models
from django.contrib.auth.models import User
from .product import Products

class Comment(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Cho phép null
    content = models.TextField()
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)  # 1 đến 5 sao
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comments/images/', null=True, blank=True)  # Thêm trường hình ảnh

    def __str__(self):
        return f'{self.user.username if self.user else "Anonymous"} - {self.content}'