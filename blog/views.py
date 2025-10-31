from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


def post_list(request):
	template = 'blog/post_list.html'
	context = {}
	posts = Post.objects.all()
	news = posts.filter(kind=Post.NEWS, is_published=True)
	announcements = posts.filter(kind=Post.ANNOUNCEMENT, is_published=True)
	drafts = posts.filter(is_published=False)
	queryset = None
	
	target = request.GET.get('filter', 'all')
	match target:
		case 'news':
			queryset = news
		case 'announcements':
			queryset = announcements
		case 'drafts':
			queryset = drafts
		case 'all':
			queryset = posts.filter(is_published=True)

	context['queryset'] = queryset
	context['announcements'] = announcements[:3]
	return render(request, template, context)


@login_required
def post_add(request):
	template = 'blog/post_add.html'
	context = {}
	form = PostForm(request.POST or None, files=request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			post = form.save()
			messages.success(request, 'Пост успішно додано')
			return redirect(post.get_absolute_url())
	context['form'] = form
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
	context['current_filter'] = 'all'  # Default for detail view
	return render(request, template, context)
