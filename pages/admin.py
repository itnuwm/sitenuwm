from django.contrib import admin
from django.contrib.auth.models import User
from .models import Webpage, WebpageRows, WebpageDocs


class WebpageRowsInline(admin.TabularInline):
    model = WebpageRows
    extra = 1
    fields = ('col1', 'col2', 'col3')
    classes = ('collapse',)


class WebpageDocsInline(admin.TabularInline):
    model = WebpageDocs
    extra = 1
    fields = ('title', 'url')
    classes = ('collapse',)


@admin.register(Webpage)
class WebpageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent', 'admin')
    list_filter = ('parent', 'admin')
    search_fields = ('title', 'slug')
    inlines = [WebpageRowsInline, WebpageDocsInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(admin__is_superuser=True)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'admin':
            kwargs['queryset'] = User.objects.exclude(is_superuser=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


