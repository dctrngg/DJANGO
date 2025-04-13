from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = RichTextField(default='', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to='static/images', null=True, blank=True)

    # Khai báo ngày cập nhật
    updated = models.DateTimeField(auto_now=True, null=True)

    # Khai báo khóa chính trong user thành khóa ngoại trong bảng Post
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
