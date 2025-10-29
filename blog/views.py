from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

def post_list(request):
	posts = Post.objects.filter(status=Post.PUBLISHED, published_date__lte=timezone.now())
	context = {
		'posts': posts
	}
	return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug, status=Post.PUBLISHED, published_date__lte=timezone.now())
	context = {
		'post': post
	}
	return render(request, 'blog/post_detail.html', context)
