from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from pages.utils import Utils
from pages.models import Webpage, Slider
from pages.forms import SliderForm, WebpageAdminForm
from django.contrib.auth.models import User
from django.http import FileResponse

import openpyxl
from io import BytesIO


@staff_member_required
def home_edit_view(request):
    template = 'adminka/home_edit.html'
    context = {}
    form = SliderForm()

    if request.method == 'POST':
        pk = request.POST.get('id')
        instance = Slider.objects.get(pk=pk) if pk else None
        if 'delete' in request.POST:
            instance.delete()
            messages.success(request, 'Банер успішно видалений')
            return redirect(request.META.get('HTTP_REFERER'))
 
        form = SliderForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Банер успішно збережений')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            for field, error in form.errors.as_data().items():
                messages.error(request, error[0].message)

    context['sliders'] = Slider.objects.all()
    context['form'] = form
    return render(request, template, context)


@staff_member_required
def user_list_view(request):
    template = 'adminka/user_list.html'
    context = {}
    context['users'] = User.objects.exclude(is_superuser=True)
    return render(request, template, context)


@staff_member_required
def sidebar_toggle_view(request, pk):
    page = get_object_or_404(Webpage, pk=pk)
    page.sidebar_edited = not page.sidebar_edited
    page.save()
    return redirect(request.META.get('HTTP_REFERER'))

@staff_member_required
def search_view(request):
    context = {}
    query = request.GET.get('q')
    if query:
        # Use multiple search approaches for better Ukrainian text matching
        from django.db.models import Q
        pages = Webpage.objects.filter(
            Q(title__icontains=query) |
            Q(title__icontains=query.lower()) |
            Q(title__icontains=query.upper()) |
            Q(title__icontains=query.capitalize())
        ).distinct()
    else:
        pages = Webpage.objects.none()
    
    context['q'] = query
    context['pages'] = pages
    return render(request, 'adminka/search_view.html', context)










##########################################################################################


@staff_member_required
@require_http_methods(['POST'])
def add_view(request):
    form = WebpageAdminForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Сторінка успішно додана')
    else:
        # print(form.errors)
        # messages.error(request, 'Помилка при додаванні сторінки')
        for field, error in form.errors.as_data().items():
            messages.error(request, error[0].message)
    return redirect(request.META.get('HTTP_REFERER', '/adminka/'))

@staff_member_required
@require_http_methods(['POST'])
def edit_view(request, pk):
    page = get_object_or_404(Webpage, pk=pk)
    form = WebpageAdminForm(request.POST or None, instance=page)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@staff_member_required
@require_http_methods(['GET'])
def delete_view(request, pk):
    page = get_object_or_404(Webpage, pk=pk)
    if page.children.count() > 0:
        messages.error(request, 'Видалення неможливе, бо сторінка має дочірні сторінки')
        return redirect(request.META.get('HTTP_REFERER', '/adminka/'))
    page.delete()
    messages.success(request, 'Сторінка успішно видалена')
    return redirect(request.META.get('HTTP_REFERER', '/adminka/'))

# 1 nuwm
# 2 struktura
# 3 navchalno-naukovi-instytuty
# 4 navchalno-naukovyi-instytut-enerhetyky-avtomatyky-ta-vodnoho-hospodarstva
# 5 kafedry
# 6 kafedra-vodnoi-inzhenerii-ta-vodnykh-tekhnolohii
# 7 zahalna-informatsiia

@staff_member_required
@require_http_methods(['GET'])
def export_pages_view(request):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'Сторінки'
    sheet.append(['ID', 'Flag', 'Admin', '1', '2', '3', '4', '5', '6', '7', 'url'])
    pages = Webpage.objects.filter(parent=None)
    for page in pages:
        flag = '✅' if page.content else '❌'
        admin = page.admin.username if page.admin else ''
        sheet.append([page.id, flag, admin, page.title, None, None, None, None, None, None, page.get_detail_url()])
        for child in page.children.all():
            flag = '✅' if child.content else '❌'
            admin = child.admin.username if child.admin else ''
            sheet.append([child.id, flag, admin, page.title, child.title, None, None, None, None, None, child.get_detail_url()])
            for level_3 in child.children.all():
                flag = '✅' if level_3.content else '❌'
                admin = level_3.admin.username if level_3.admin else ''
                sheet.append([level_3.id, flag, admin, page.title, child.title, level_3.title, None, None, None, None, level_3.get_detail_url()])
                for level_4 in level_3.children.all():
                    flag = '✅' if level_4.content else '❌'
                    admin = level_4.admin.username if level_4.admin else ''
                    sheet.append([level_4.id, flag, admin, page.title, child.title, level_3.title, level_4.title, None, None, None, level_4.get_detail_url()])
                    for level_5 in level_4.children.all():
                        flag = '✅' if level_5.content else '❌'
                        admin = level_5.admin.username if level_5.admin else ''
                        sheet.append([level_5.id, flag, admin, page.title, child.title, level_3.title, level_4.title, level_5.title, None, None, level_5.get_detail_url()]) 
                        for level_6 in level_5.children.all():
                            flag = '✅' if level_6.content else '❌'
                            admin = level_6.admin.username if level_6.admin else ''
                            sheet.append([level_6.id, flag, admin, page.title, child.title, level_3.title, level_4.title, level_5.title, level_6.title, None, level_6.get_detail_url()])
                            for level_7 in level_6.children.all():
                                flag = '✅' if level_7.content else '❌'
                                admin = level_7.admin.username if level_7.admin else ''
                                sheet.append([level_7.id, flag, admin, page.title, child.title, level_3.title, level_4.title, level_5.title, level_6.title, level_7.title, level_7.get_detail_url()])
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='pages.xlsx')

@staff_member_required
@require_http_methods(['POST'])
def slug_edit_view(request, pk):
    page = get_object_or_404(Webpage, pk=pk)
    if request.POST.get('slug'):
        slug = Utils.slugify(request.POST['slug'])
        siblings = page.parent.children.filter(slug=slug)
        if siblings.count() > 0:
            messages.error(request, 'Цей slug вже зайнятий')
        else:
            page.slug = slug
            page.save()
            messages.success(request, 'Slug успішно змінений')
    return redirect(request.META.get('HTTP_REFERER', '/adminka/'))

@staff_member_required
@require_http_methods(['POST'])
def design_edit_view(request, pk):
    page = get_object_or_404(Webpage, pk=pk)
    if request.POST.get('design'):
        design = request.POST['design']
        if design in [choice[0] for choice in Webpage.DESIGN_CHOICES]:
            page.design = design
            page.save()
            messages.success(request, 'Дизайн успішно змінений')
    return redirect(request.META.get('HTTP_REFERER', '/adminka/'))

@staff_member_required
@require_http_methods(['POST'])
def admin_edit_view(request, pk):
    page = get_object_or_404(Webpage, pk=pk)
    if not request.POST.get('admin'):
        messages.error(request, 'Не вказано адміна')
        return redirect(request.META.get('HTTP_REFERER', '/adminka/'))

    admin = request.POST['admin'].strip()
    if not admin.endswith('@nuwm.edu.ua'):
        messages.error(request, 'Невірна електронна адреса адміна')
        return redirect(request.META.get('HTTP_REFERER', '/adminka/'))

    admin, created = User.objects.get_or_create(username=admin)
    if created:
        admin.set_password(admin.username)
        admin.save()

    page.admin = admin
    page.save()
    messages.success(request, f'Адмін успішно змінений')
    return redirect(request.META.get('HTTP_REFERER', '/adminka/'))














@staff_member_required
def adminka_0_view(request):
    context = {}
    page = None
    form = WebpageAdminForm(initial={'parent': page})
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    context['form'] = form
    return render(request, 'adminka/adminka_view.html', context)

@staff_member_required
def adminka_1_view(request, slug):
    page = get_object_or_404(Webpage, parent=None, slug=slug)
    context = {}
    form = WebpageAdminForm(initial={'parent': page})
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    context['form'] = form
    return render(request, 'adminka/adminka_view.html', context)

@staff_member_required
def adminka_2_view(request, slug1, slug2):
    page = get_object_or_404(Webpage, parent__slug=slug1, slug=slug2)
    context = {}
    form = WebpageAdminForm(initial={'parent': page})
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    context['form'] = form
    return render(request, 'adminka/adminka_view.html', context)

@staff_member_required
def adminka_3_view(request, slug1, slug2, slug3):
    page = get_object_or_404(Webpage, parent__slug=slug2, slug=slug3)
    context = {}
    form = WebpageAdminForm(initial={'parent': page})
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    context['form'] = form
    return render(request, 'adminka/adminka_view.html', context)

@staff_member_required
def adminka_4_view(request, slug1, slug2, slug3, slug4):
    page = get_object_or_404(Webpage, parent__slug=slug3, slug=slug4)
    context = {}
    form = WebpageAdminForm(initial={'parent': page})
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    context['form'] = form
    return render(request, 'adminka/adminka_view.html', context)

@staff_member_required
def adminka_5_view(request, slug1, slug2, slug3, slug4, slug5):
    page = get_object_or_404(Webpage, parent__slug=slug4, slug=slug5)
    context = {}
    form = WebpageAdminForm(initial={'parent': page})
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    context['form'] = form
    return render(request, 'adminka/adminka_view.html', context)

@staff_member_required
def adminka_6_view(request, slug1, slug2, slug3, slug4, slug5, slug6):
    page = get_object_or_404(Webpage, parent__slug=slug5, slug=slug6)
    context = {}
    form = WebpageAdminForm(initial={'parent': page})
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    context['form'] = form
    return render(request, 'adminka/adminka_view.html', context)

@staff_member_required
def adminka_7_view(request, slug1, slug2, slug3, slug4, slug5, slug6, slug7):
    page = get_object_or_404(Webpage, parent__slug=slug6, slug=slug7)
    context = {}
    form = WebpageAdminForm(initial={'parent': page})
    context['page'] = page
    context['children'] = Webpage.objects.filter(parent=page).order_by('id')
    context['form'] = form
    context['THE_END'] = True
    return render(request, 'adminka/adminka_view.html', context)