from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post


def post_list(request):
	template = 'blog/post_list.html'
	context = {}
	posts = Post.objects.all()
	context['posts'] = posts.filter(is_published=True)
	context['news'] = posts.filter(kind=Post.NEWS, is_published=True)
	context['announcements'] = posts.filter(kind=Post.ANNOUNCEMENT, is_published=True)
	context['drafts'] = posts.filter(is_published=False)
	return render(request, template, context)


def post_detail(request, slug):
	template = 'blog/post_detail.html'
	context = {}
	post = get_object_or_404(Post, slug=slug)
	context['post'] = post

	posts = Post.objects.all()
	context['posts'] = posts.filter(is_published=True)
	context['news'] = posts.filter(kind=Post.NEWS, is_published=True)
	context['announcements'] = posts.filter(kind=Post.ANNOUNCEMENT, is_published=True)
	context['drafts'] = posts.filter(is_published=False)
	return render(request, template, context)
