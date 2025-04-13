from django.shortcuts import render, get_object_or_404

from ..models.models import Post


def post_list(request):
    posts = Post.objects.all()
    print(posts)
    return render(request, 'post.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

def video(request):
    return render(request, 'video.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def cart(request):
    return render(request, 'cart.html')