from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from system.decorators import perms_required
from .models import Webpage
from .forms import WebpageForm, WebpageRowsFormset, WebpageDocsFormset


@perms_required('pages.add')
@require_http_methods(['GET', 'POST'])
def add_view(request, pk):
    parent = get_object_or_404(Webpage, pk=pk)
    if not request.user.is_superuser and parent.admin != request.user:
        return HttpResponseForbidden()
    form = WebpageForm(request.POST or None, files=request.FILES or None, initial={'parent': parent})
    if request.method == 'POST':
        if form.is_valid():
            page = form.save()
            messages.success(request, 'Сторінка успішно додана')
            return redirect(page.get_detail_url())
    context = {}
    context['page'] = parent
    context['form'] = form
    return render(request, 'pages/add_view.html', context)


@login_required
def edit_view(request, pk):
    page = get_object_or_404(Webpage, pk=pk)
    if not request.user.is_superuser and page.admin != request.user:
        return HttpResponseForbidden()
    form = WebpageForm(request.POST or None, request.FILES or None, instance=page)
    rows = WebpageRowsFormset(request.POST or None, queryset=page.rows.all(), initial=[{'webpage': page}], prefix='rows')
    docs = WebpageDocsFormset(request.POST or None, queryset=page.docs.all(), initial=[{'webpage': page}], prefix='docs')
    if request.method == 'POST':
        if form.is_valid() and rows.is_valid() and docs.is_valid():
            page = form.save()
            rows.save()
            docs.save()
            if request.POST.get('redirect') == 'false':
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect(page.get_detail_url())
        else:
            print(form.errors)
            print(rows.errors)
            print(docs.errors)
    context = {}
    context['page'] = page
    context['form'] = form
    context['rows'] = rows
    context['docs'] = docs
    return render(request, 'pages/edit_view.html', context)


@staff_member_required
@require_http_methods(['POST'])
def delete_view(request, pk):
    page = get_object_or_404(Webpage, pk=pk)
    page.delete()
    messages.success(request, 'Сторінка успішно видалена')
    return redirect(request.META.get('HTTP_REFERER'))


def layer_1_view(request, slug):
    page = get_object_or_404(Webpage, parent=None, slug=slug)
    context = {}
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    return render(request, f'pages/{page.design}_view.html', context)

def layer_2_view(request, slug1, slug2):
    page = get_object_or_404(Webpage, parent__slug=slug1, slug=slug2)
    context = {}
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    return render(request, f'pages/{page.design}_view.html', context)

def layer_3_view(request, slug1, slug2, slug3):
    page = get_object_or_404(Webpage, parent__slug=slug2, slug=slug3)
    context = {}
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    return render(request, f'pages/{page.design}_view.html', context)

def layer_4_view(request, slug1, slug2, slug3, slug4):
    page = get_object_or_404(Webpage, parent__slug=slug3, slug=slug4)
    context = {}
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    return render(request, f'pages/{page.design}_view.html', context)

def layer_5_view(request, slug1, slug2, slug3, slug4, slug5):
    page = get_object_or_404(Webpage, parent__slug=slug4, slug=slug5)
    context = {}
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    return render(request, f'pages/{page.design}_view.html', context)

def layer_6_view(request, slug1, slug2, slug3, slug4, slug5, slug6):
    page = get_object_or_404(Webpage, parent__slug=slug5, slug=slug6)
    context = {}
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    return render(request, f'pages/{page.design}_view.html', context)

def layer_7_view(request, slug1, slug2, slug3, slug4, slug5, slug6, slug7):
    page = get_object_or_404(Webpage, parent__slug=slug6, slug=slug7)
    context = {}
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    return render(request, f'pages/{page.design}_view.html', context)